from curses.ascii import NUL
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Article, Comment, Folder, Good, Tag, TagArrow
from .forms import PostForm,CreateFolderForm,FindForm,CommentForm,CreateTagForm,CreateTagArrowForm

# Create your views here.
@login_required(login_url='/admin/login/')
def index(request, page=1):
    if request.method == 'POST':
        form = FindForm(request.POST)
        find = request.POST['find']
        print("index request.method == 'POST'")
        articles= get_article(request.user, page, find)
    else:
        form = FindForm()
        articles= get_article(request.user, page)

     # 共通処理
    params = {
        'login_user':request.user,
        'form':form,
        'contents':articles,
    }
    return render(request, 'weblib/index.html', params)

# Create your views here.
@login_required(login_url='/admin/login/')
def mypage(request, page=1):
    if request.method == 'POST':
        form = FindForm(request.POST)
        find = ""
        if 'find' in request.POST:
            find = request.POST['find']
            articles= get_article(request.user, page, find, mypage=True)
        if 'tag_id' in request.POST:
            tag_id = request.POST['tag_id']
            tag = get_tag_id(request.user, tag_id)
            articles= get_article2(request.user, tag , page, find, mypage=True)
        print("mypage request.method == 'POST'")
    else:
        form = FindForm()
        articles= get_article(request.user, page, mypage=True)

     # 共通処理
    tags = get_tag(request.user)
    form_tag = CreateTagForm()
    form_tagarrow = CreateTagArrowForm(request.user)
    article_tagarrows = []
    for article in articles:
        tagarrow = get_tagarrow(request.user, article)
        if tagarrow is None:
            article_tagarrows.append("")
        else:
            article_tagarrows.append(tagarrow.tag)
    
    #print(article_tagarrows)

    params = {
        'login_user':request.user,
        'form':form,
        'contents':articles,
        'article_tagarrows':article_tagarrows,
        'tags':tags,
        'form_tag':form_tag,
        'form_tagarrow':form_tagarrow,
    }
    return render(request, 'weblib/mypage.html', params)

# Articleのポスト処理
@login_required(login_url='/admin/login/')
def post(request):
    # POST送信の処理
    if request.method == 'POST':
        # 送信内容の取得
        folder_name = request.POST['folder_id']
        title = request.POST['title']
        content = request.POST['content']
        keyword = request.POST['keyword']
        link = request.POST['link']
        public = 'public' in request.POST
        # Folderの取得
        folder = Folder.objects.filter(owner=request.user) \
                .filter(title=folder_name).first()
        if folder == None:
            folder_id = -1
        else:
            folder_id = folder.id
        # Articleを作成し設定して保存
        article = Article()
        article.owner = request.user
        article.title = title
        article.content = content
        article.keyword = keyword
        article.link = link
        article.public = public
        article.folder = folder_id
        article.save()
        # メッセージを設定
        messages.success(request, '新しいweb記事の投稿に成功しました')
        print("post request.method == 'POST'");
        return redirect(to='/weblib/mypage')
    
    # GETアクセス時の処理
    else:
        form = PostForm(request.user)
    
    # 共通処理
    params = {
        'login_user':request.user,
        'form':form,
    }
    return render(request, 'weblib/post.html', params)

# Articleの編集処理
@login_required(login_url='/admin/login/')
def edit(request, article_id):
    # POST送信の処理
    if request.method == 'POST':
        article_cp = get_article_id(article_id)
        # 送信内容の取得
        folder_name = request.POST['folder_id']
        title = request.POST['title']
        content = request.POST['content']
        keyword = request.POST['keyword']
        link = request.POST['link']
        public = 'public' in request.POST
        # Folderの取得
        folder = Folder.objects.filter(owner=request.user) \
                .filter(title=folder_name).first()
        if folder == None:
            folder_id = -1
        else:
            folder_id = folder.id
        # Articleを作成し設定して保存
        article = Article()
        article.id = article_cp.id
        article.owner = request.user
        article.title = title
        article.content = content
        article.keyword = keyword
        article.link = link
        article.public = public
        article.folder = folder_id
        article.pub_date = article_cp.pub_date
        article.save()
        # メッセージを設定
        messages.success(request, 'web記事の更新に成功しました')
        print("post request.method == 'POST'");
        return redirect(to='/weblib/mypage')
    
    # GETアクセス時の処理
    else:
        article = get_article_id(article_id)
        initial_values = {
            'title': article.title,
            'content': article.content,
            'keyword': article.keyword,
            'link': article.link,
            'public': article.public,
            'folder_id': article.folder_id,
        }
        form = PostForm(request.user, initial=initial_values)
        """
        form.title = article.title
        form.content = article.content
        form.keyword = article.keyword
        form.link = article.link
        form.public = article.public
        """
        print(article.title)
        #print(form.title)
        #form.folder = article.folder_id
    
    # 共通処理
    params = {
        'login_user':request.user,
        'form':form,
        'id':article_id,
    }
    return render(request, 'weblib/edit.html', params)

# Articleの削除処理
@login_required(login_url='/admin/login/')
def delete(request, article_id):
    article = get_article_id(article_id)
    # POST送信の処理
    if request.method == 'POST':
        article.delete()
        # メッセージを設定
        messages.success(request, 'web記事の削除に成功しました')
        print("delete request.method == 'POST'");
        return redirect(to='/weblib/mypage')
    # 共通処理
    params = {
        'login_user':request.user,
        'item':article,
        'id':article_id,
    }
    return render(request, 'weblib/delete.html', params)

# Articleの詳細, commentの送信
@login_required(login_url='/admin/login/')
def detail(request, article_id=-1):
    article = get_article_id(article_id)
    
    if request.method == 'POST':
        content = request.POST['content']
        if(content!=''):
            comment = Comment()
            comment.owner = request.user
            comment.article = article
            comment.content = content
            comment.save()
            print("detail request.method == 'POST'")
    
    # 共通処理
    form = CommentForm()
    comments = get_comment(article)

    params = {
        'login_user':request.user,
        'item':article,
        'form':form,
        'comments':comments,
    }
    return render(request, 'weblib/detail.html', params)

# Commentの削除処理
@login_required(login_url='/admin/login/')
def delete_comment(request, comment_id):
    comment = get_comment_id(comment_id)
    article = get_article_id(comment.article.id)

    # POST送信の処理
    if request.user == comment.owner:
        comment.delete()
        print("delete_comment request.method == 'POST'")
        # メッセージを設定
        messages.success(request, 'コメントの削除に成功しました')
        
    return redirect(to='/weblib/detail/'+str(article.id))

#tagの作成
def make_tag(request):
    
    # POST送信の処理
    if request.method == 'POST':
        content = request.POST['content']
        if(content!=''):
            tag = Tag()
            tag.owner = request.user
            tag.title = content
            tag.save()
            print("detail request.method == 'POST'")


        # メッセージを設定
        messages.success(request, 'タグを作成しました')
        print("make_tag request.method == 'POST'");
        return redirect(to='/weblib/mypage')

#tagの作成
def make_tagarrow(request, article_id=-1):
    article = get_article_id(article_id)
    _tagarrow = get_tagarrow(request.user, article)
  
    # POST送信の処理
    if request.method == 'POST':
        content = request.POST['content']
        # Tagの取得
        tag = Tag.objects.filter(owner=request.user) \
                .filter(title=content).first()
        tagarrow = TagArrow()
        if tag is None:
            if(content=='-'):
                if _tagarrow is not None:
                    #print("タグを破棄しました");
                    #messages.success(request, 'タグを破棄しました')
                    _tagarrow.delete()
            return redirect(to='/weblib/mypage')
        if _tagarrow is None:
            print("make_tagarrow first");
            tagarrow.owner = request.user
            tagarrow.tag = tag
            tagarrow.article = article
            tagarrow.save()
        else:
            print("make_tagarrow change");
            tagarrow.id = _tagarrow.id
            tagarrow.owner = request.user
            tagarrow.tag = tag
            tagarrow.article = article
            tagarrow.save()

        # メッセージを設定
        #messages.success(request, 'タグを付与しました')
        return redirect(to='/weblib/mypage')

#-----------------------関数----------------------------------

# 指定されたグループおよび検索文字によるArticleの取得
def get_article(owner, page=1, find='', mypage=False):
    page_num=8
    if(mypage==False):
        if(find==''):
            articles = Article.objects.filter(public=True).all().reverse()
        else:
            articles = Article.objects.filter(public=True).filter(keyword__contains=find).all().reverse()
    else:
        if(find==''):
            articles = Article.objects.filter(owner=owner).all().reverse()
        else:
            articles = Article.objects.filter(owner=owner).filter(keyword__contains=find).all().reverse()

    # ページネーションで指定ページを取得
    page_item = Paginator(articles, page_num)
    return page_item.get_page(page)

# 指定されたグループおよび検索文字によるArticleの取得
def get_article2(owner, tag, page=1, find='', mypage=False):
    page_num=8

    tagarrows = get_tagarrows(owner, tag)
    tagarrows_articleIds = []
    for tagarrow in tagarrows:
        tagarrows_articleIds.append(tagarrow.article.id)

    if(mypage==False):
        if(find==''):
            articles = Article.objects.filter(public=True).all().reverse()
        else:
            articles = Article.objects.filter(public=True).filter(keyword__contains=find).all().reverse()
    else:
        if(find==''):
            articles = Article.objects.filter(owner=owner, id__in = tagarrows_articleIds).all().reverse()
        else:
            articles = Article.objects.filter(owner=owner, id__in = tagarrows_articleIds).filter(keyword__contains=find).all().reverse()

    # ページネーションで指定ページを取得
    page_item = Paginator(articles, page_num)
    return page_item.get_page(page)

def get_article_id(article_id=-1):
    article = Article.objects.get(id=article_id)
    
    return article

#コメントの取得
def get_comment(article):
    comments = Comment.objects.filter(article=article).all()
    return comments

def get_comment_id(comment_id=-1):
    comment = Comment.objects.get(id=comment_id)
    return comment

#tagの取得
def get_tag(owner):
    tags = Tag.objects.filter(owner=owner).all()

    return tags

def get_tag_id(owner, tag_id=-1):
    tag = Tag.objects.filter(owner=owner, id=tag_id).first()

    return tag

#tagarrowの取得
def get_tagarrow(owner, article):
    tagarrow = TagArrow.objects.filter(owner=owner, article = article).first()

    return tagarrow

def get_tagarrows(owner, tag):
    tagarrows = TagArrow.objects.filter(owner=owner, tag=tag).all()

    return tagarrows

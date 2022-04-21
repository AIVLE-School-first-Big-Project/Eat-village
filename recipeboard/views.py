from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from recipeboard.models import Recipeboard, Recipecomment, User
from django.core.paginator import Paginator
from django.db.models import Q, Count, F
from recipeboard.forms import Recipeboardform, Recipecommentform
from django.utils import timezone


def recipeboard_index(request): #레시피게시글 목록

    kw = request.GET.get('kw', '') #키워드 검색기능
    so = request.GET.get('so', 'recent')
    page = request.GET.get('page', '1')

    if kw:
        board_list = Recipeboard.objects.filter(
            Q(title__icontains=kw) |
            Q(nickname__icontains=kw) |
            Q(ingredient__icontains=kw) |
            Q(detail__icontains=kw)
        ).distinct()
    else:
        board_list = Recipeboard.objects.all()

    if so == 'view': #조회순 정렬
        board_list = board_list.order_by('-view', '-time')
    elif so == 'recommended': #추천순 정렬
        board_list = board_list.order_by('-recommended', '-time')
    elif so == 'recent': #기본정렬: 등록순
        board_list = board_list.order_by('-boardid')

    paginator = Paginator(board_list, 20) #페이징기준
    page_obj = paginator.get_page(page)
    last_page = page_obj.paginator.page_range[-1]

    context = {'board_list' : page_obj,
               'last_page':last_page,
               'kw':kw,
               'page':page,
               'so':so
               }

    return render(request, 'recipeboard/recipeboard_index.html', context)


def recipeboard_detail(request, boardid): # 게시글 내용, 댓글생성
    
    board = get_object_or_404(Recipeboard, pk=boardid)

    if request.method == "GET":
        recipecommentform = Recipecommentform()

    comment = Recipecomment.objects.filter(
        boardid = boardid,
        parentcommentid__isnull = True
    )
    babycomment = Recipecomment.objects.filter(
        boardid = boardid,
        parentcommentid__isnull = False
    )

    commentcount = Recipecomment.objects.filter(boardid=boardid).count()

    if request.method == 'POST':
        # if request.POST.get('comment'):
        recipecommentform = Recipecommentform(request.POST)
        if recipecommentform.is_valid():
            newcomment = Recipecomment(**recipecommentform.cleaned_data)
            # newcomment.userid = request.user
            newcomment.boardid = boardid
            newcomment.time = timezone.now()
            newcomment.save()
        return redirect('recipeboard:recipeboard_detail', boardid=boardid)

    context = {
        'board' : board,
        'comment' : comment,
        'babycomment' : babycomment,
        'recipecommentform' : recipecommentform,
        'commentcount': commentcount,
    }
    return render(request, 'recipeboard/recipeboard_detail.html', context)


def recipeboard_comment(request, boardid, commentid): #댓글자세히보기, 대댓글 내용과 생성
    
    comment = get_object_or_404(Recipecomment, pk=commentid)
    
    babycomment = Recipecomment.objects.filter(
        boardid = boardid,
        parentcommentid = commentid
    )

    if request.method == "GET":
        recipecommentform = Recipecommentform()

    if request.method == 'POST':
        recipecommentform = Recipecommentform(request.POST)
        if recipecommentform.is_valid():
            newbabycomment = Recipecomment(**recipecommentform.cleaned_data)
            # newbabycomment.userid = request.user
            newbabycomment.parentcommentid = commentid
            newbabycomment.boardid = boardid
            newbabycomment.time = timezone.now()
            newbabycomment.save()
        return redirect('recipeboard:recipeboard_comment', boardid=boardid, commentid=commentid)
    
    context = {
        'boardid' : boardid,
        'comment' : comment,
        'babycomment' : babycomment,
        'recipecommentform' : recipecommentform
    }
    
    return render(request, 'recipeboard/recipeboard_comment.html', context)

def recipecomment_delete(request, commentid):

    # current_user_id = request.session['userid']
    # current_user = User.objects.get(userid=current_user_id)

    comment = get_object_or_404(Recipecomment, pk=commentid)

    # if 현재유저 != 댓글쓴유저:
    #    messages.warning(request, '권한없음')
    # else: 
    comment.detail = '삭제된 댓글입니다.'
    comment.save()
    boardid = comment.boardid

    return redirect('recipeboard:recipeboard_detail', boardid=boardid)


def recipeboard_create(request): #게시물생성

    if request.method == "POST":
        form = Recipeboardform(request.POST)
        if form.is_valid():
            board = Recipeboard(**form.cleaned_data)
            board.time = timezone.now()
            '''
            board.userid = request.user
            #로그인 유저 정보 받기
            '''
            board.recommended = 0
            board.view = 0
            board.save()
            return redirect('recipeboard:recipeboard_index')
    else:
        form = Recipeboardform()
    
    context = {'form': form}

    return render(request, 'recipeboard/recipeboard_create.html', context)


def recipeboard_update(request, boardid): #게시물수정

    board = get_object_or_404(Recipeboard, pk=boardid)

    # if request.user != board.userid:
    #     messages.error(request, '권한없음')
    #     return redirect('recipeboard:recipeboard_detail', boardid=boardid)
    
    if request.method == "POST":
        form = Recipeboardform(request.POST, instance=board)
        if form.is_valid():
            board.title = form.cleaned_data['title']
            board.ingredient = form.cleaned_data['ingredient']
            board.detail = form.cleaned_data['detail']
            board.save()
            return redirect('recipeboard:recipeboard_detail', boardid=boardid)
    else:
        form = Recipeboardform(instance=board)

    context = {'form': form}

    return render(request, 'recipeboard/recipeboard_create.html', context)


def recipeboard_delete(request, boardid): #게시물삭제

    board = get_object_or_404(Recipeboard, pk=boardid)

    # if request.user != board.userid:
    #     messages.error(request, '권한없음')
    #     return redirect('recipeboard:recipeboard_detail', boardid=boardid)
    
    board.delete()

    return redirect('recipeboard:recipeboard_index')





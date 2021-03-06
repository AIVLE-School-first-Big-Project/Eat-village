from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from users.models import Recipeboard, Recipeboardimage, Recipecomment, Userrecommendedcommunity
from django.core.paginator import Paginator
from django.db.models import Q
from recipeboard.forms import Recipeboardform, Recipecommentform, Recipeboardimageform
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def recipeboard_index(request): # 레시피게시글 목록

    kw = request.GET.get('kw', '') # 키워드 검색기능
    so = request.GET.get('so', '')
    page = request.GET.get('page', '1')

    if kw:
        board_list = Recipeboard.objects.all().filter(
            Q(title__contains=kw) |
            Q(ingredient__contains=kw) |
            Q(detail__contains=kw)
        )
    else:
        board_list = Recipeboard.objects.all()
 
    if so == 'view': # 조회순 정렬
        board_list = board_list.order_by('-view', '-boardid')
    elif so == 'recommended': # 추천순 정렬
        board_list = board_list.order_by('-recommended', '-boardid')
    else:
        board_list = board_list.order_by('-boardid')

    paginator = Paginator(board_list,10) # 페이징기준
    page_obj = paginator.get_page(page)

    today = timezone.now().date
    context = {'board_list' : page_obj,
               'kw':kw,
               'page':page,
               'so':so,
               'today':today,
               }

    return render(request, 'recipeboard/recipeboard_index.html', context)

@login_required
def recipeboard_detail(request, boardid): # 게시글 내용, 댓글생성
    
    user = request.user
    board = get_object_or_404(Recipeboard, pk=boardid)
    images = Recipeboardimage.objects.filter(boardid=boardid)

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
    likedata = Userrecommendedcommunity.objects.filter(userid=user, boardid=board).first()

    if request.method == 'POST':
        # if request.POST.get('comment'): # 댓글달기
        recipecommentform = Recipecommentform(request.POST)
        if recipecommentform.is_valid():
            newcomment = Recipecomment(**recipecommentform.cleaned_data)
            newcomment.userid = request.user
            newcomment.boardid = board
            newcomment.time = timezone.now()
            newcomment.save()
        return redirect('recipeboard:recipeboard_detail', boardid=boardid)

    context = {
        'user' : user,
        'board' : board,
        'comment' : comment,
        'babycomment' : babycomment,
        'recipecommentform' : recipecommentform,
        'commentcount': commentcount,
        'images' : images,
        'likedata' : likedata,
    }

    response = render(request, 'communityboard/communityboard_detail.html', context)
    if board.userid != user:
        cookie_name = f'view:{request.user.id}'
        tomorrow = timezone.now().replace(hour=23, minute=59, second=0)
        expires = tomorrow
        if request.COOKIES.get(cookie_name) is not None:
            cookies = request.COOKIES.get(cookie_name)
            cookies_list = cookies.split('|')
            if str(boardid) not in cookies_list:
                response.set_cookie(cookie_name, cookies + f'|{boardid}', expires =expires)
                board.view += 1
                board.save()
                return response
        else:
            response.set_cookie(cookie_name, boardid, expires =expires)
            board.view += 1
            board.save()
            return response

    return render(request, 'recipeboard/recipeboard_detail.html', context)

@login_required
def recipeboard_recommend(request, boardid):
    user = request.user
    board = get_object_or_404(Recipeboard, pk=boardid)
    if request.method == "POST":
        Userrecommendedcommunity.objects.create(userid=user, boardid=board)
        board.recommended += 1
        board.save()
    return redirect('recipeboard:recipeboard_detail', boardid=boardid)

@login_required
def recipeboard_recommendcancel(request, boardid):
    user = request.user
    board = get_object_or_404(Recipeboard, pk=boardid)
    likedata = Userrecommendedcommunity.objects.filter(userid=user, boardid=board).first()
    if request.method == "POST":
        likedata.delete()
        board.recommended -= 1
        board.save()
    return redirect('recipeboard:recipeboard_detail', boardid=boardid)

@login_required
def recipeboard_comment(request, boardid, commentid): # 댓글자세히보기, 대댓글 내용과 생성
    
    comment = get_object_or_404(Recipecomment, pk=commentid)
    board = get_object_or_404(Recipeboard, pk=boardid)

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
            newbabycomment.userid = request.user
            newbabycomment.parentcommentid = commentid
            newbabycomment.boardid = board
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

@login_required
def recipecomment_delete(request, commentid):

    # current_user_id = request.session['userid']
    # current_user = User.objects.get(userid=current_user_id)

    comment = get_object_or_404(Recipecomment, pk=commentid)

    deletedcommentmessage = '삭제된 댓글입니다.'

    if request.user != comment.userid:
        messages.warning(request, '권한없음')
    else: 
        comment.detail = deletedcommentmessage
        comment.save()

    return redirect('recipeboard:recipeboard_detail', boardid=comment.boardid.boardid)

@login_required
def recipeboard_create(request): # 게시물생성

    Imageformset = modelformset_factory(Recipeboardimage, form=Recipeboardimageform, extra=3)

    if request.method == "POST":
        form = Recipeboardform(request.POST)
        formset = Imageformset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            board = Recipeboard(**form.cleaned_data)
            board.userid = request.user
            board.recommended = 0
            board.view = 0
            board.time = timezone.now()
            board.save()
            for form in formset:
                image = Recipeboardimage(**form.cleaned_data)
                image.boardid = board
                image.time = timezone.now()
                image.save()
        # messages.success(request, "작성완료!")
        return redirect('recipeboard:recipeboard_index')
    else:
        form = Recipeboardform()
        formset = Imageformset(queryset=Recipeboardimage.objects.none())
    
    context = {'form': form,
               'formset': formset}

    return render(request, 'recipeboard/recipeboard_create.html', context)

@login_required
def recipeboard_update(request, boardid): # 게시물수정

    board = get_object_or_404(Recipeboard, pk=boardid)
    Imageformset = modelformset_factory(Recipeboardimage, form=Recipeboardimageform, extra=0)

    if request.user != board.userid:
        messages.error(request, '권한없음')
        return redirect('recipeboard:recipeboard_detail', boardid=boardid)
    
    if request.method == "POST":
        form = Recipeboardform(request.POST, instance=board)
        formset = Imageformset(request.POST, request.FILES)
        if form.is_valid():
            board.title = form.cleaned_data['title']
            board.ingredient = form.cleaned_data['ingredient']
            board.detail = form.cleaned_data['detail']
            board.save()
            formset.save()
            return redirect('recipeboard:recipeboard_detail', boardid=boardid)
    else:
        form = Recipeboardform(instance=board)
        formset = Imageformset(queryset=Recipeboardimage.objects.filter(boardid=boardid))

    context = {'form': form, 'formset':formset}

    return render(request, 'recipeboard/recipeboard_create.html', context)

@login_required
def recipeboard_delete(request, boardid): # 게시물삭제

    board = get_object_or_404(Recipeboard, pk=boardid)

    if request.user != board.userid:
        messages.error(request, '권한없음')
        return redirect('recipeboard:recipeboard_detail', boardid=boardid)
    
    board.delete()

    return redirect('recipeboard:recipeboard_index')




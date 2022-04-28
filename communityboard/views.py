from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from users.models import Communityboard, Communitycomment, Communityboardimage
from django.core.paginator import Paginator
from django.db.models import Q, Count, F
from communityboard.forms import Communityboardform, Communitycommentform, Communityboardimageform
from django.utils import timezone

# Create your views here.
def communityboard_index(request): #레시피게시글 목록

    kw = request.GET.get('kw', '') #키워드 검색기능
    so = request.GET.get('so', '')
    page = request.GET.get('page', '1')
    header = request.GET.get('header', '')
    address = request.GET.get('address', '')

    if kw:
        board_list = Communityboard.objects.all().filter(
            Q(title__contains=kw) |
            Q(detail__contains=kw)
        )
    else:
        board_list = Communityboard.objects.all()
 
    if so == 'view': #조회순 정렬
        board_list = board_list.order_by('-view', '-boardid')
    else: 
        board_list = board_list.order_by('-boardid')


    if header == 'h1' : #재료나눔게시판
        board_list = board_list.filter(header='요리재료게시판')
    elif header == 'h2' : #자유게시판
        board_list = board_list.filter(header='자유게시판')
    elif header == '':
        board_list = board_list.order_by('-boardid')

    user = request.user

    if address == 'my':
        board_list = board_list.filter(user__address = user.address)
    
    paginator = Paginator(board_list, 10) #페이징기준
    page_obj = paginator.get_page(page)
    # last_page = page_obj.paginator.page_range[-1]

    context = {'user':user,
               'board_list' : page_obj,
            #    'last_page':last_page,
               'kw':kw,
               'page':page,
               'so':so,
               'address':address,
               'header':header,
               }

    return render(request, 'communityboard/communityboard_index.html', context)


def communityboard_detail(request, boardid): # 게시글 내용, 댓글생성
    
    user = request.user
    board = get_object_or_404(Communityboard, pk=boardid)
    images = Communityboardimage.objects.filter(boardid=boardid)

    if request.method == "GET":
        communitycommentform = Communitycommentform()

    board.view += 1 ## 조회수증가
    board.save()

    comment = Communitycomment.objects.filter(
        boardid = boardid,
        parentcommentid__isnull = True
    )
    babycomment = Communitycomment.objects.filter(
        boardid = boardid,
        parentcommentid__isnull = False
    )

    commentcount = Communitycomment.objects.filter(boardid=boardid).count()

    if request.method == 'POST':
        # if request.POST.get('comment'): #댓글달기
        communitycommentform = Communitycommentform(request.POST)
        if communitycommentform.is_valid():
            newcomment = Communitycomment(**communitycommentform.cleaned_data)
            newcomment.userid = request.user
            newcomment.boardid = board
            newcomment.time = timezone.now()
            newcomment.save()
        return redirect('communityboard:communityboard_detail', boardid=boardid)

    context = {
        'user' : user,
        'board' : board,
        'comment' : comment,
        'babycomment' : babycomment,
        'communitycommentform' : communitycommentform,
        'commentcount': commentcount,
        'images' : images,
    }
    return render(request, 'communityboard/communityboard_detail.html', context)

# def communityboard_recommend(request, boardid):
#     user = request.user
#     board = get_object_or_404(communityboard, pk=boardid)
#     if request.method == "POST":
#         Userrecommendedcommunity.objects.create(userid=user, boardid=board)
#         board.recommended += 1
#         board.save()
#     return redirect('communityboard:communityboard_detail', boardid=boardid)

# def communityboard_recommendcancel(request, boardid):
#     user = request.user
#     board = get_object_or_404(communityboard, pk=boardid)
#     likedata = Userrecommendedcommunity.objects.filter(userid=user, boardid=board).first()
#     if request.method == "POST":
#         likedata.delete()
#         board.recommended -= 1
#         board.save()
#     return redirect('communityboard:communityboard_detail', boardid=boardid)

def communityboard_comment(request, boardid, commentid): #댓글자세히보기, 대댓글 내용과 생성
    
    comment = get_object_or_404(Communitycomment, pk=commentid)
    board = get_object_or_404(Communityboard, pk=boardid)

    babycomment = Communitycomment.objects.filter(
        boardid = boardid,
        parentcommentid = commentid
    )

    if request.method == "GET":
        communitycommentform = Communitycommentform()

    if request.method == 'POST':
        communitycommentform = Communitycommentform(request.POST)
        if communitycommentform.is_valid():
            newbabycomment = Communitycomment(**communitycommentform.cleaned_data)
            newbabycomment.userid = request.user
            newbabycomment.parentcommentid = commentid
            newbabycomment.boardid = board
            newbabycomment.time = timezone.now()
            newbabycomment.save()
        return redirect('communityboard:communityboard_comment', boardid=boardid, commentid=commentid)
    
    context = {
        'boardid' : boardid,
        'comment' : comment,
        'babycomment' : babycomment,
        'communitycommentform' : communitycommentform
    }
    
    return render(request, 'communityboard/communityboard_comment.html', context)

def communitycomment_delete(request, commentid):

    comment = get_object_or_404(Communitycomment, pk=commentid)

    deletedcommentmessage = '삭제된 댓글입니다.'

    if request.user != comment.userid:
       messages.warning(request, '권한없음')
    else: 
        comment.detail = deletedcommentmessage
        comment.save()

    return redirect('communityboard:communityboard_detail', boardid=comment.boardid.boardid)

# from .forms import Imageformset
def communityboard_create(request): #게시물생성

    Imageformset = modelformset_factory(Communityboardimage, form=Communityboardimageform, extra=1)

    if request.method == "POST":
        form = Communityboardform(request.POST)
        formset = Imageformset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            board = Communityboard(**form.cleaned_data)
            if request.user.is_authenticated:
                board.userid = request.user
            board.recommended = 0
            board.view = 0
            board.time = timezone.now()
            board.save()
            # formset.instance = board
            # formset.save()
            for form in formset:
                image = Communityboardimage(**form.cleaned_data)
                image.boardid = board
                image.time = timezone.now()
                image.save()
            # messages.success(request, "작성완료!")
            return redirect('communityboard:communityboard_index')
    else:
        form = Communityboardform()
        formset = Imageformset(queryset=Communityboardimage.objects.none())
    
    context = {'form': form,
               'formset': formset}

    return render(request, 'communityboard/communityboard_create.html', context)


def communityboard_update(request, boardid): #게시물수정

    board = get_object_or_404(Communityboard, pk=boardid)
    Imageformset = modelformset_factory(Communityboardimage, form=Communityboardimageform, extra=0)

    if request.user != board.userid:
        messages.error(request, '권한없음')
        return redirect('communityboard:communityboard_detail', boardid=boardid)
    
    if request.method == "POST":
        form = Communityboardform(request.POST, instance=board)
        formset = Imageformset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            board.title = form.cleaned_data['title']
            board.detail = form.cleaned_data['detail']
            board.save()
            formset.save()
            # for form in formset:
            #     image = communityboardimage(**form.cleaned_data)
            #     image.time = timezone.now()
            #     image.save()
            return redirect('communityboard:communityboard_detail', boardid=boardid)
    else:
        form = Communityboardform(instance=board)
        formset = Imageformset(queryset=Communityboardimage.objects.filter(boardid=boardid))

    context = {'form': form, 'formset':formset}

    return render(request, 'communityboard/communityboard_create.html', context)


def communityboard_delete(request, boardid): #게시물삭제

    board = get_object_or_404(Communityboard, pk=boardid)

    if request.user != board.userid:
        messages.error(request, '권한없음')
        return redirect('communityboard:communityboard_detail', boardid=boardid)
    
    board.delete()

    return redirect('communityboard:communityboard_index')

# def upload_community_img(request, boardid): #이미지 업로드

#     board = communityboard.objects.filter(boardid=boardid)
#     if request.method == 'POST':
#         image = request.FILES.get('img-file')
#         time = timezone.now()

#         communityboard.objects.create(boardid=board, image=image, time=time)
    

from django.shortcuts import render, redirect, get_object_or_404
from .models import Posting, Comment
from .forms import PostingForm, CommentForm
# [코드 작성] login_required 데코레이션 추가
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'page/index.html')

# [Read] 전체 글 목록 보기
def posting_list(request):
    postings = Posting.objects.all()
    context = {
        'postings': postings,
    }
    return render(request, 'page/posting_list.html', context)

# [Create] 글 작성하기
def posting_create(request):
    # [코드 작성] 웹 페이지에 로그인이 되어있는 경우만 글 쓰기가 가능하도록 조건문 작성
    if request.user.is_authenticated:
        if request.method == 'POST':
            posting_form = PostingForm(request.POST)
            
            if posting_form.is_valid():
                # [코드 작성] posting_form에 작성자 객체 추가
                posting_form = posting_form.save(commit=False)
                posting_form.author = request.user
                posting_form.save()
                return redirect('page:posting_list')
        else:
            posting_form = PostingForm()
        
        context = {
            'posting_type': '글쓰기',
            'posting_form': posting_form,
        }
        return render(request, 'page/posting_form.html', context)
    # [코드 작성] 로그인이 되어있지 않은 경우 로그인 페이지로 돌아가도록 처리
    return redirect('account:login')

# [Read & Create] 작성글 보기 & 댓글 작성
def posting_detail(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.posting = posting
            # [코드 작성] comment_form에 작성자 객체 추가
            comment.author = request.user
            comment.save()
            return redirect('page:posting_detail', posting_id)
    else :
        comment_form = CommentForm()
    
    comments = posting.comment_list.all()

    context = {
        'posting': posting,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'page/posting_detail.html', context)
    
# [Update] 작성글 수정
# [코드 작성] login_required 데코레이션 추가

def posting_update(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    # [코드 작성] 글 작성자가 로그인한 사람과 같을 경우에만 글 수정이 가능하도록 조건문 작성
    
    if request.method == 'POST':
        posting_form = PostingForm(request.POST, instance=posting)

        if posting_form.is_valid():
            posting_form.save()
            return redirect('page:posting_detail', posting_id)
    else:
        posting_form = PostingForm(instance=posting)

    context = {
        'posting_type': '글수정',
        'posting': posting,
        'posting_form': posting_form,
    }
    return render(request, 'page/posting_form.html', context)
    # [코드 추가] posting_id에 해당하는 페이지로 redirect


# [Delete] 작성글 삭제
# [코드 작성] login_required 데코레이션 추가
@login_required
def posting_delete(request, posting_id):
    if request.method == 'POST':
        posting = get_object_or_404(Posting, id=posting_id)
        posting.delete()
        return redirect('page:posting_list')
    return redirect('page:posting_detail', posting_id)

# [Delete] 댓글 삭제
# [코드 작성] login_required 데코레이션 추가
@login_required
def comment_delete(request, posting_id, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return redirect('page:posting_detail', posting_id)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Comment, Hashtag, Active_hashtag
from .forms import MovieForm, CommentForm
from django.views.decorators.http import require_POST, require_safe, require_http_methods

@require_http_methods(['GET'])
def index(request):
    movies = Movie.objects.all()[::-1]
    hashtag = Active_hashtag.objects.all().distinct().values_list('hashtag')
    hash = []
    for i in hashtag:
        hash.append(Hashtag.objects.filter(pk=i[0]))
    context = {
        'movies': movies,
        'hash': hash,
    }
    return render(request, 'movies/index.html', context)


@require_http_methods(['POST','GET'])
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
             # hash tag 저장
            for word in movie.description.split(): # 공백을 기준으로 리스트
                if word[0] == '#':
                    # word랑 같은 해시태그가 존재하면 기존 객체 반환, 없으면 새로운 객체 생성
                    hashtag, created = Hashtag.objects.get_or_create(content=word)
                    # 1. 현재 등록된 모든 해시태그 보기
                    # 2. 클릭 시 hashtag 기준으로 filter 해주기
                    # 3. 게시물 수정 시, 새로 등록된 해시태그 검사 해주기                      
                    movie.hashtags.add(hashtag)
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()
        hash = Hashtag.objects.all()

    context = {
        'form': form,
        'hash': hash,
    }
    return render(request, 'movies/create.html', context)

def hashtag_filter(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)

    movies = hashtag.movie_set.order_by('-pk')
    hashtag_list = Active_hashtag.objects.all().distinct().values_list('hashtag')
    hash = []
    for i in hashtag_list:
        hash.append(Hashtag.objects.filter(pk=i[0]))
    context = {
        'hash': hashtag_list,
        'hashtag' : hashtag,
        'movies' : movies,
    }
    return render(request, 'movies/hashtag.html', context)

@require_http_methods(['GET'])
def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = movie.comment_set.all()
    # Select * from comment where parent is NULL;
    comments = movie.comment_set.filter(parent__isnull=True) # 대댓글
    context = {
        'movie': movie,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'movies/detail.html', context)


@require_http_methods(['POST'])
def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.delete()
    return redirect('movies:index')


@require_http_methods(['POST','GET'])
def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'movies/update.html', context)



@require_http_methods(['POST'])
def comments_create(request, pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        parent_pk = request.POST.get('parent_pk')
        if comment_form.is_valid():
            comment = comment_form.save(commit=False) # comment_form는 article과 user행 정보는 안받은 상태(exclude 되어있음)
            comment.movie = movie # 비어있는 칼럼에 정보 추가
            comment.user = request.user
            if parent_pk:
                parent = Comment.objects.get(pk=parent_pk)
                comment.parent = parent
            comment.save()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')

@require_http_methods(['POST'])
def comments_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('articles:detail', pk)

@require_http_methods(['POST'])
def likes(request, movie_pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=movie_pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
        return redirect('movies:detail', movie_pk)
    return redirect('accounts:login')


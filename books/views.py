from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_http_methods, require_POST
from .models import Book
from .forms import BookForm
import os
import anthropic
from dotenv import load_dotenv
from django.contrib import messages
load_dotenv()

# Create your views here.
# 전체 도서 목록
@require_safe # 도서 조회 
def index(request):
    books = Book.objects.all().order_by('-pk')
    return render(request, 'books/index.html', {'books' : books})

@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('books:detail', book.pk)
    else:
        form = BookForm()
    return render(request, 'books/create.html', {'form': form})

@require_safe
def detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/detail.html', {'book':book})

@login_required
@require_http_methods(['GET', 'POST'])    
def update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.user != request.user:
        return redirect('books:detail', book.pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:detail', book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/update.html', {'form':form, 'book':book})

@login_required
@require_POST
def delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.user == request.user:
        book.delete()
    return redirect('books:index')

@login_required
@require_POST
def generate_author_info(request, pk):
    book = get_object_or_404(Book, pk=pk)

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        messages.error(request, 'API 키가 설정되지 않았어요.')
        return redirect('books:detail', book.pk)

    prompt = (
        f"'{book.author}' 작가에 대해 3~4문장으로 소개해줘. "
        "확실하지 않은 내용은 지어내지 말고, 모르면 모른다고 말해줘."
    )

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model='claude-sonnet-5-5',
            max_tokens=500,
            messages=[{'role': 'user', 'content': prompt}],
        )
        book.author_info = response.content[0].text
        book.save()
    except Exception:
        messages.error(request, '작가 정보를 가져오지 못했어요. 잠시 후 다시 시도해 주세요.')

    return redirect('books:detail', book.pk)

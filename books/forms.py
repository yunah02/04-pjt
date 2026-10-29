from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'description', 'customer_review_rank')
        labels = {
            'title': '도서 제목',
            'author': '저자',
            'description': '설명',
            'customer_review_rank': '회원 리뷰 평점 (0~10)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'customer_review_rank': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
        }
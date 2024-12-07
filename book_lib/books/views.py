from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm

def index(request):
    books = Book.objects.all()
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'books/index.html', {'books': books, 'form': form})

def add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'books/index.html', {'form': form})

def delete(request, book_id):
    Book.objects.filter(id=book_id).delete()
    return redirect('home')

def edit(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit.html', {'form': form, 'book': book})
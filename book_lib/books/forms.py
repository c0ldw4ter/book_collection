from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book','title','date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}) 
        }
from django.db import models

class Book(models.Model):
    book = models.CharField(max_length=100, verbose_name="Название книги")
    title = models.CharField(max_length=100, verbose_name="Имя автора")
    date = models.DateField(verbose_name="Дата издания")

    def __str__(self):
        return self.book
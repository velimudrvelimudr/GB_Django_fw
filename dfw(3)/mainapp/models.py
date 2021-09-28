from django.db import models

# Create your models here.


class BookCategory(models.Model):
    name = models.CharField(verbose_name='Название', max_length=32, unique=True)
    description = models.CharField(verbose_name='Описание', max_length=512, blank=True)

    def __str__(self):
        return f'{self.name}, {self.description}'


class Books(models.Model):
    cat_fk = models.ForeignKey(BookCategory, on_delete=models.    CASCADE)
    name = models.CharField(verbose_name='Заголовок', max_length=256)
    author = models.CharField(verbose_name='Автор(ы)', max_length=255, blank=True)
    annotation = models.TextField(verbose_name='Аннотация', blank=True)
    cover = models.ImageField(upload_to='covers', verbose_name='Обложка', blank=True)
    created_at = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлён', auto_now=True)

    def __str__(self):
        return f'{self.name}, {self.author}\n{self.annotation}\n{self.cat_fk.name}'


    @property
    def book_count(self):
        """ Определяет, сколько пользователей добавили книгу в свою библиотеку.  """

        return len(self.booklib.all())


# Пока продрался через все дебри методов, вот создал первый рабочий пример. Сам по себе он ни в звезду, ни в красную армию, ибо дублирует __str__, но раз уж сделал, пусть пока остаётся.
    @property
    def book_info(self):
        """ Собирает всю информацию о книге и выводит её в виде текстовой строки.  """

        return f"""Полная информация о книге.\n \
            Название: {self.name};\n \
            Автор: {self.author if self.author else 'отсутствует;'};\n \
            Аннотация: {self.annotation if self.annotation else 'отсутствует'};\n \
            Добавлена в библиотеку: {self.created_at};\n \
            Обновлена: {self.updated_at}; \
            Входит в категорию: {self.cat_fk.name}."""


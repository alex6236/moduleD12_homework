from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache
# from django.shortcuts import render


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя пользователя')
    ratingAuthor = models.SmallIntegerField(default=0, verbose_name='Рейтинг')
    
    def __str__(self):
        return self.authorUser.username
    
    class Meta:
        verbose_name = 'Автора'
        verbose_name_plural = 'Авторы'

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating')) or 0 # type: ignore
        pRat = 0
        pRat += postRat.get('postRating') # type: ignore

        commentRat = self.authorUser.comment_set.all( # type: ignore
        ).aggregate(commentRating=Sum('rating')) or 0
        cRat = 0
        cRat += commentRat.get('commentRating') # type: ignore
        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Категории' )
    subscribers = models.ManyToManyField(User)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.name
    


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(
        max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dataCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения')
    postCategory = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категории')
    title = models.CharField(max_length=124, verbose_name='Заголовок')
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:123] + '...'
    
    def get_absolute_url(self):
        return f'/news/{self.id}'  # type: ignore
    
    # Кэширование на низком уровне
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сохраняем новый объект
        cache.delete(f'post-{self.pk}') # удаляем старый из кэша
   
    
    def __str__(self):
        categories = ', '.join([str(category) for category in self.postCategory.all()])
        return f"Заголовок: {self.title} |Дата: {self.dataCreation} |Автор: {self.author.authorUser.username} |Категория: {categories}"
 


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.categoryThrough    


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


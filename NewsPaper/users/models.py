
# from django.db import models
# # from datetime import datetime
# from django.contrib.auth.models import User
# from news.models import Category

    
# class Subscriber(models.Model):
#     subscriber = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Подписчик")
#     # subscriber = models.CharField(verbose_name="Подписчик", max_length=100)
#     email = models.EmailField(verbose_name="Почта", unique=True, blank=True)
#     category = models.ManyToManyField(Category)
#     # category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name="Категории")
#     date = models.DateTimeField(verbose_name="Дата подписки", auto_now_add=True)
    
#     class Meta:
#         verbose_name = 'Подписчик'
#         verbose_name_plural = 'Подписчики'

#     def __str__(self):
#         return f'{self.subscriber} | {self.email} | {self.category} |{self.date}'
    
    

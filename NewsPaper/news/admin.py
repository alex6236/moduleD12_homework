from django.contrib import admin
from .models import Post, Category, Author

class PostAdmin(admin.ModelAdmin):
    
    def post_categories(self, obj):
        return ', '.join([str(category) for category in obj.postCategory.all()])
    
    post_categories.short_description = 'Категории'
    
    list_display = ('author', 'title', 'post_categories', 'dataCreation')
    list_filter = ('author', 'postCategory')
    search_fields = ('author__authorUser__username', 'title')
    
class CategoryAdmin(admin.ModelAdmin):
    def number_of_subscribers(self, obj):
        return obj.subscribers.count()

    number_of_subscribers.short_description = 'Количество подписчиков'

    list_display = ('name', 'number_of_subscribers')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')
    
    
    
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)

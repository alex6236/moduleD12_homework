from datetime import datetime, timezone
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Post, Category
from django_filters.views import FilterView
from .filters import PostFilter
from .forms import DateFilterForm, TitleFilterForm, TtextFilterForm, UsernameFilterForm, AddPostForm
# =========================
from django.db.models import Q
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# =======================================
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
# ======================================
from django.utils import timezone
from django.urls import reverse
# =============================
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)



class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now(timezone.utc)
        return context
# ====================================================    
 
class AddPost(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = AddPostForm
    permission_required = ('news.add_post' )
    template_name = 'add_post.html'
    success_url = '/news/'
    # login_url = '/accounts/login/'
    login_url = '/signup/login_site/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now(timezone.utc)
        context['form'] = AddPostForm() 
        return context
    
    def get_post_today(self):
        today = datetime.now().date()
        post_limit = Post.objects.filter(author=self.request.user.author,  # type: ignore
                                         dataCreation__date=today).count()
        return post_limit
    
    def form_valid(self, form):
        if self.get_post_today() >= 3:
           return redirect(reverse('post_limit'))
        else:
            self.object = form.save(commit=False)
            self.object.author = self.request.user.author # type: ignore
            self.object.save()
            category = form.cleaned_data['category']
            self.object.postCategory.add(category) 
            return super().form_valid(form)
    
def post_limit(request):
    return render(request, 'post_limit.html')

    
class PostUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = AddPostForm
    permission_required = ('news.change_post')
    template_name = 'edit_post.html'
    success_url = '/news/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        category = form.cleaned_data['category']
        self.object.postCategory.add(category)
        return super().form_valid(form)

    

class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = ('news.delete_post')
    template_name = 'delete_post.html'
    success_url = '/news/'

# ==============================================

class NewsDetail(DetailView):
    model = Post
    template_name ='news_detail.html'
    context_object_name = 'news_detail'
    
    # Кэширование на низком уровне
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None) 
       
        obj = super().get_object(queryset=self.queryset) 
        cache.set(f'post-{self.kwargs["pk"]}', obj)
        
        return obj

    
class LoremDetail(DetailView):
    model = Post
    template_name ='lorem_post.html'
    context_object_name = 'lorem_post'

class PostSearch(FilterView):
    model = Post
    filterset_class = PostFilter
    template_name = 'search_site.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter
        results = self.filterset.qs if self.request.GET else Post.objects.none()
        context['results'] = results.order_by('-dataCreation')
        context['date'] = DateFilterForm(self.request.GET or None) 
        context['title'] = TitleFilterForm(self.request.GET or None) 
        context['username'] = UsernameFilterForm(self.request.GET or None) 
        context['text'] = TtextFilterForm(self.request.GET or None) 
        return context

    
class SearchHeader(FilterView):
    model = Post
    template_name = 'search_2.html'
    paginate_by = 2
    # filterset_class = PostFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        if q:  
            multiple_q = Q(
                Q(title__iregex=q) |
                Q(author__authorUser__username__iregex=q) |
                Q(text__iregex=q))
            results = Post.objects.filter(multiple_q).order_by('-id')
            paginator = Paginator(results, self.paginate_by)
            page_number = self.request.GET.get('page')
            context['results'] = paginator.get_page(page_number)
        return context
    
# ==================================

class CategoryNewsView(ListView):
    model = Post
    template_name = 'category.html'
    paginate_by = 2
    
    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = Category.objects.get(id=category_id)
        return category.post_set.all().order_by('-id') # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category_id = self.kwargs['category_id']
        category = Category.objects.get(id=category_id)
        context['category'] = category
        context['is_subscribed'] = category.subscribers.filter(id=user.id).exists() # type: ignore
       
        return context
    
    # def get(self, request, category_id):
    #     user = request.user
    #     category = Category.objects.get(id=category_id)
    #     posts = category.post_set.all().order_by('-id') # type: ignore
    #     is_subscribed = category.subscribers.filter(id=user.id).exists()
    #     context = {
    #     'category': category,
    #     'posts': posts,
    #     'is_subscribed': is_subscribed,
    #     }
    #     return render(request, 'category.html', context)
    
@login_required
def subscribe_category(request, category_id):
    user = request.user
    # print(user, user.id)
    category = Category.objects.get(id=category_id)
    # print(category)
    if not category.subscribers.filter(id=user.id).exists():
        email = user.email
        # print(email)
        category.subscribers.add(user)
        html = render_to_string('mail/subscribed.html',
            {'category': category, 'user': user,},)
        msg = EmailMultiAlternatives(
            subject=f'Подписка на новости',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email, ],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
        return redirect(category.get_absolute_url())
    return redirect(category.get_absolute_url())

@login_required
def unsubscribe_category(request, category_id):
    user = request.user
    category = Category.objects.get(id=category_id)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    return redirect(category.get_absolute_url()) 


  

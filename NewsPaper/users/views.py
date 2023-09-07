from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from news.models import Author, Category
import logging

logger = logging.getLogger(__name__)

class AccountsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribed_categories'] = Category.objects.filter(subscribers=self.request.user)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists() # type: ignore
        return context
    

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)  # type: ignore
        Author.objects.create(authorUser=user)
    return redirect('users:profile')





from .models import Post, PostCategory, Category
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# =====================================================


def get_categories(instance):
    categories = instance.postCategory.all()
    return ', '.join([str(category) for category in categories])


@receiver(m2m_changed, sender=Post.postCategory.through)
def new_post_subscribers(sender, instance, **kwargs):

    if kwargs['action'] == 'post_add':
        subscribers = instance.postCategory.values('subscribers__email', 'subscribers__username',)
        categories = get_categories(instance)
        # print(subscribers)
        html = render_to_string('mail/new_post_subscribers.html',
                                context={'category': categories, 
                                         'post': instance, 
                                         })
        subject = f"Новая публикация в Вашей подписке."
        
        for subscriber in subscribers:
            send_email_notification(subject, html, subscriber['subscribers__email'])
           
            
def send_email_notification(subject, html, recipient):
 
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()



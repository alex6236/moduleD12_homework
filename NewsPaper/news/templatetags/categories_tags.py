from django import template
from news.models import Category
# from users.forms import SubscriberForm

register = template.Library()


@register.inclusion_tag('categories.html')
def all_categories():
    cats = Category.objects.all()
    return {"cats": cats}

cat_dist = {
            'sports': 'Спорт',
            'politics': 'Политика',
            'education': 'Образование',
            'technology': 'Технологии',
            'lorem': 'Рыба-текст',
        }

@register.filter(name='trans_category')
def get_value_dict(category):
    for key, value in cat_dist.items():
        if key == category:
            return value
    return ''





from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category
import logging
 
logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = 'Удаление всех постов из категории по команде (python manage.py remove_all_posts_from_category arg) вместо arg ввести название категории (lorem, technology, education, politics, sports)'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        category_name = options['category']
        answer = input(f'Вы правда хотите удалить все статьи в категории {category_name}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        try:
            category = Category.objects.get(name=category_name)
            Post.objects.filter(postCategory=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Успешно удалил все новости из категории {category.name}'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не удалось найти категорию'))
 

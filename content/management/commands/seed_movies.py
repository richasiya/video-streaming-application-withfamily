from django.core.management.base import BaseCommand
from content.models import Content, Category

class Command(BaseCommand):
    help = 'Seed the database with sample movie content'

    def handle(self, *args, **options):
        cat, _ = Category.objects.get_or_create(name='Sample')
        created = 0
        for i in range(1, 51):
            title = f"Sample Movie {i}"
            description = f"This is the description for {title}. A short summary to use in demos."
            video_url = "https://www.youtube.com/embed/dQw4w9WgXcQ"  # placeholder embeddable link
            obj, created_flag = Content.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'content_type': 'movie',
                    'category': cat,
                    'video_url': video_url,
                }
            )
            if created_flag:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created} sample movies'))

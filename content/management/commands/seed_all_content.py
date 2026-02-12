import os
import io
import random
import base64
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from content.models import Content, Category

# Uses picsum.photos to fetch random placeholder images
IMAGE_SIZES = {
    'movie': (600, 900),
    'webseries': (600, 900),
    'shortfilm': (600, 900),
    'social': (600, 600),
}

PLACEHOLDER_VIDEO = "https://www.youtube.com/embed/dQw4w9WgXcQ"

# Tiny 1x1 transparent PNG (base64)
TINY_PNG = base64.b64decode(
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII='
)


class Command(BaseCommand):
    help = 'Seed content for all types (movies, webseries, shortfilm, social) with poster images. Ensures 50 items per type.'

    def fetch_image(self, seed, w, h):
        # Try requests if available (with timeout), otherwise use urllib with timeout
        url = f"https://picsum.photos/seed/{seed}/{w}/{h}"
        self.stdout.write(f"Fetching {url} ...")
        try:
            import requests
            resp = requests.get(url, timeout=8)
            resp.raise_for_status()
            return resp.content
        except Exception:
            try:
                from urllib.request import urlopen
                resp = urlopen(url, timeout=8)
                return resp.read()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to fetch image {url}: {e}"))
                return None

    def ensure_category(self):
        cat, _ = Category.objects.get_or_create(name='Sample')
        return cat

    def create_item(self, idx, kind, category):
        title = f"{kind.capitalize()} Sample {idx}"
        description = f"This is a sample {kind} called {title}. Description for demo."
        slug_base = f"{kind}-sample-{idx}"

        obj, created_flag = Content.objects.get_or_create(
            title=title,
            defaults={
                'description': description,
                'content_type': kind,
                'category': category,
                'video_url': PLACEHOLDER_VIDEO,
            }
        )
        # Ensure slug saved
        if not obj.slug:
            obj.save()

        # If thumbnail missing, fetch and attach
        if not obj.thumbnail:
            w, h = IMAGE_SIZES.get(kind, (600, 900))
            seed = f"{kind}-{idx}-{random.randint(1,9999)}"
            data = self.fetch_image(seed, w, h)
            if not data:
                # fallback to tiny png
                data = TINY_PNG
            filename = f"{obj.slug or slug_base}.jpg"
            try:
                obj.thumbnail.save(filename, ContentFile(data), save=True)
            except Exception as e:
                # If saving fails, write a warning
                self.stdout.write(self.style.WARNING(f"Failed to save thumbnail for {obj}: {e}"))
        return created_flag

    def handle(self, *args, **options):
        category = self.ensure_category()
        total_created = 0
        target = 50
        for kind in ['movie', 'webseries', 'shortfilm', 'social']:
            existing = Content.objects.filter(content_type=kind).count()
            if existing >= target:
                self.stdout.write(self.style.NOTICE(f"{kind}: already has {existing} items, skipping."))
                continue
            start_idx = existing + 1
            created_for_kind = 0
            for i in range(start_idx, target + 1):
                created = self.create_item(i, kind, category)
                if created:
                    total_created += 1
                    created_for_kind += 1
            self.stdout.write(self.style.SUCCESS(f"Seeded {created_for_kind} new items for {kind} (now {Content.objects.filter(content_type=kind).count()})"))
        self.stdout.write(self.style.SUCCESS(f"Total new items created: {total_created}"))

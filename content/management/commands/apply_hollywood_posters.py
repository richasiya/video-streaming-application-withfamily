import random
import base64
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from content.models import Content

# Tiny 1x1 transparent PNG (base64) as fallback
TINY_PNG = base64.b64decode(
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII='
)


class Command(BaseCommand):
    help = 'Apply Hollywood-style poster placeholders to movie Content thumbnails'

    def fetch_image(self, seed, w, h):
        url = f"https://picsum.photos/seed/{seed}/{w}/{h}"
        self.stdout.write(f"Fetching {url} ...")
        # Use urllib with a short timeout and a couple retries to avoid long hangs
        from urllib.request import urlopen, Request
        from urllib.error import URLError, HTTPError
        headers = {'User-Agent': 'Mozilla/5.0'}
        for attempt in range(2):
            try:
                req = Request(url, headers=headers)
                with urlopen(req, timeout=6) as resp:
                    return resp.read()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Attempt {attempt+1} failed for {url}: {e}"))
        return None

    def handle(self, *args, **options):
        movies = Content.objects.filter(content_type='movie')
        if not movies.exists():
            self.stdout.write(self.style.NOTICE('No movie content found to update.'))
            return
        updated = 0
        for idx, movie in enumerate(movies, start=1):
            # Use movie.slug if available for stable seeds
            seed = f"hollywood-{movie.slug or movie.id}-{random.randint(1,9999)}"
            w, h = (600, 900)
            data = self.fetch_image(seed, w, h)
            if not data:
                data = TINY_PNG
            filename = f"{movie.slug or 'movie-' + str(movie.id)}.jpg"
            try:
                # Overwrite existing thumbnail
                movie.thumbnail.save(filename, ContentFile(data), save=True)
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"Updated poster for: {movie.title}"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to save poster for {movie}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Finished. Posters updated for {updated} movies."))

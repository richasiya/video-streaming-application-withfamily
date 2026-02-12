from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Content(models.Model):
    CONTENT_TYPES = [
        ('movie', 'Movie'),
        ('webseries', 'Web Series'),
        ('shortfilm', 'Short Film'),
        ('podcast', 'Podcast'),
    ]
    ACCESS_LEVELS = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    access_level = models.CharField(
        max_length=20,
        choices=ACCESS_LEVELS,
        default='free'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    # YouTube / external video
    video_url = models.URLField(blank=True, null=True)

    # Local uploaded video
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)

    slug = models.SlugField(max_length=250, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # Auto slug generator
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200]
            slug = base
            counter = 1
            while Content.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('content_watch', kwargs={'slug': self.slug})

    @property
    def video_src(self):
        # 1️⃣ Local video (highest priority)
        if self.video_file:
            try:
                return self.video_file.url
            except:
                pass

        # 2️⃣ YouTube / external URL
        if self.video_url:
            url = self.video_url.strip()

            # youtube watch link
            if "youtube.com/watch" in url:
                video_id = url.split("v=")[-1].split("&")[0]
                return f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&modestbranding=1"

            # youtu.be short link
            if "youtu.be/" in url:
                video_id = url.split("youtu.be/")[-1].split("?")[0]
                return f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&modestbranding=1"

            # already embed
            if "youtube.com/embed/" in url:
                return url.replace("youtube.com", "youtube-nocookie.com")

            # other platforms (vimeo, cdn, direct mp4)
            return url

        return None


class SiteConfig(models.Model):
    site_name = models.CharField(max_length=100, default='withFamily')
    logo = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        help_text='Logo displayed under navbar on main page'
    )

    def __str__(self):
        return f"SiteConfig: {self.site_name}"

    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'

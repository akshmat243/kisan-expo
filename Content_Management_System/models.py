from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import uuid


class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    template = models.CharField(max_length=100, default='default.html')
    content = RichTextField(blank=True)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Page.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

class Section(models.Model):
    SECTION_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('faq', 'FAQ'),
        ('custom', 'Custom HTML'),
    ]

    page = models.ForeignKey(Page, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES, default='text')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.page.title} - {self.title} ({self.section_type})"

class Image(models.Model):
    section = models.ForeignKey(Section, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cms/images/')
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.section.title} - {self.caption or 'Image'}"

class Video(models.Model):
    section = models.ForeignKey(Section, related_name='videos', on_delete=models.CASCADE)
    video_url = models.URLField()
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.section.title} - Video"

class FAQ(models.Model):
    section = models.ForeignKey(Section, related_name='faqs', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = RichTextField()

    def __str__(self):
        return self.question

class Banner(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='cms/banners/')
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    message = RichTextField()
    image = models.ImageField(upload_to='cms/testimonials/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

class MetaTag(models.Model):
    page = models.OneToOneField(Page, related_name='meta_tags', on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    meta_keywords = models.TextField(blank=True)

    def __str__(self):
        return f"SEO for {self.page.title}"

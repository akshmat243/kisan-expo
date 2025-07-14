# cms/admin.py
from django.contrib import admin
from .models import Page, Section, Image, Video, FAQ, Banner, Testimonial, MetaTag

class SectionInline(admin.StackedInline):
    model = Section
    extra = 0

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'publish_date')
    list_filter = ('is_published',)
    search_fields = ('title',)
    readonly_fields = ('slug', 'created_at', 'updated_at')
    inlines = [SectionInline]

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'page', 'section_type', 'is_active', 'order')
    list_filter = ('section_type', 'is_active')
    search_fields = ('title',)
    inlines = [ImageInline]

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'section')

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'display_order')
    list_filter = ('is_active',)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_at')

class MetaTagAdmin(admin.ModelAdmin):
    list_display = ('page', 'meta_title')

admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(MetaTag, MetaTagAdmin)

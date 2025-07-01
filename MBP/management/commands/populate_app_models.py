from django.core.management.base import BaseCommand
from django.apps import apps
from django.utils.text import slugify
from ...models import AppModel

class Command(BaseCommand):
    help = 'Populate AppModel with all installed models.'

    def handle(self, *args, **kwargs):
        created = 0
        for model in apps.get_models():
            model_name = model.__name__
            app_label = model._meta.app_label
            if not AppModel.objects.filter(name=model_name, app_label=app_label).exists():
                AppModel.objects.create(
                    name=model_name,
                    app_label=app_label,
                    slug=slugify(model_name),
                    verbose_name=model._meta.verbose_name.title()
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} models added."))

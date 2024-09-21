import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    Provides fixtures loading functionality configurable via
    settings variable "FIXTURES".

    Minimal settings example:
        FIXTURES = {
            'labels': [ 'fixtures1', 'fixtures2' ]
        }

    Settings example with image directories:
        FIXTURES = {
            'labels': ['fixtures1', 'fixtures2'],
            'media': [
                {
                    'src': BASE_DIR / 'my_app' / 'fixtures' / 'images',
                    'dest': MEDIA_ROOT / 'my_app' / 'images',
                },
                {
                    'src': BASE_DIR / 'my_other_app' / 'fixtures' / 'files',
                    'dest': MEDIA_ROOT / 'my_other_app' / 'files',
                },
            ],
        }
    """

    help = 'Load fixtures'

    def handle(self, *args, **options):
        if self._has_valid_settings():
            call_command('loaddata', *settings.FIXTURES['labels'])
            self._upload_media_files()
        else:
            self.stdout.write(self.style.ERROR(
                'In order to use "load_fixtures" command, you must '
                'set FIXTURES settings variable and it must a valid '
                'dictionary with "labels" list or tuple'
            ))

    @staticmethod
    def _has_valid_settings() -> bool:
        return (
            hasattr(settings, 'FIXTURES')
            and isinstance(settings.FIXTURES, dict)
            and 'labels' in settings.FIXTURES
            and isinstance(settings.FIXTURES['labels'], (list, tuple))
        )

    def _upload_media_files(self):
        for images_dir in settings.FIXTURES.get('media', []):
            src_dir = images_dir['src']
            dest_dir = images_dir['dest']
            # Ensure the destination directory exists
            os.makedirs(dest_dir, exist_ok=True)

            # Copy all files from src_dir to dest_dir
            for filename in os.listdir(src_dir):
                src_file = os.path.join(src_dir, filename)
                dest_file = os.path.join(dest_dir, filename)
                if os.path.isfile(src_file):
                    shutil.copy(src_file, dest_file)

            self.stdout.write(self.style.SUCCESS(
                f'Successfully copied files from {src_dir} to {dest_dir}'
            ))

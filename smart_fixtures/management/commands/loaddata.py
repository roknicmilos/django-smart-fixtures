import os
import shutil

from django.conf import settings
from django.core.management.commands.loaddata import Command as LoadDataCommand
from django.db import DEFAULT_DB_ALIAS, connections


class Command(LoadDataCommand):
    """
    Provides fixtures loading functionality configurable via
    settings variable "FIXTURES".

    Overrides the default Django `loaddata` management command
    to provide additional functionality for copying media files
    to the MEDIA_ROOT directory.

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

    help = (
        'Overrides loaddata command to add '
        '--all flag for loading all fixtures'
    )

    def add_arguments(self, parser):
        self._add_base_class_arguments(parser)
        parser.add_argument(
            '--all',
            action='store_true',
            help=(
                'Load all fixtures specified in '
                '"FIXTURES" settings variable'
            ),
        )

    @staticmethod
    def _add_base_class_arguments(parser):
        """
        We override this method by copying all arguments from base
        class and making the `fixture` argument optional.
        """
        parser.add_argument(
            'args', metavar='fixture', nargs='*', help='Fixture labels.'
        )
        parser.add_argument(
            '--database',
            default=DEFAULT_DB_ALIAS,
            choices=tuple(connections),
            help=(
                'Nominates a specific database to load fixtures into. '
                'Defaults to the "default" database.'
            ),
        )
        parser.add_argument(
            '--app',
            dest='app_label',
            help='Only look for fixtures in the specified app.',
        )
        parser.add_argument(
            '--ignorenonexistent',
            '-i',
            action='store_true',
            dest='ignore',
            help=(
                'Ignores entries in the serialized data for fields '
                'that do not currently exist on the model.'
            ),
        )
        parser.add_argument(
            '-e',
            '--exclude',
            action='append',
            default=[],
            help=(
                'An app_label or app_label.ModelName to exclude. '
                'Can be used multiple times.'
            ),
        )
        parser.add_argument(
            '--format',
            help='Format of serialized data when reading from stdin.',
        )

    def handle(self, *fixture_labels, **options):
        if options['all']:
            if not self._has_valid_settings():
                self._print_invalid_settings_error()
            else:
                self._upload_media_files()
                fixture_labels = settings.FIXTURES['labels']

        super().handle(*fixture_labels, **options)

    @staticmethod
    def _has_valid_settings() -> bool:
        return (
            hasattr(settings, 'FIXTURES')
            and isinstance(settings.FIXTURES, dict)
            and 'labels' in settings.FIXTURES
            and isinstance(settings.FIXTURES['labels'], (list, tuple))
        )

    def _print_invalid_settings_error(self):
        self.stdout.write(self.style.ERROR(
            'In order to use "loaddata" command with "--all" flag, '
            'you must set FIXTURES settings variable and it must a '
            'valid dictionary with "labels" list or tuple'
        ))

    def _upload_media_files(self):
        copied_files = []
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
                    copied_files.append((src_file, dest_file))

        if copied_files:
            self._print_copied_files(copied_files)
        else:
            self.stdout.write('No media files to copy')

    def _print_copied_files(
        self, file_path_pairs: list[tuple[str, str]]
    ) -> None:
        copied_files_display = [
            f"{index + 1}. {relative_src} -> {relative_dest}\n"
            for index, (relative_src, relative_dest)
            in enumerate([
                (
                    self._get_relative_path(src),
                    self._get_relative_path(dest)
                ) for src, dest in file_path_pairs
            ])
        ]
        self.stdout.write(
            f'Successfully copied files:\n{"".join(copied_files_display)}'
        )

    @staticmethod
    def _get_relative_path(absolute_path: str) -> str:
        relative_path = absolute_path.replace(str(settings.BASE_DIR), '')
        return (
            relative_path[1:]
            if relative_path.startswith('/')
            else relative_path
        )

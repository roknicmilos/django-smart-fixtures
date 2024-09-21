# Django Smart Fixtures

**DON'T BE STUPID, AND LOAD FIXTURES IN A SMART WAY!**

## Purpose

This Django package provides `load_fixtures` management command that allows you
to **load fixtures in a more convenient way**. It uses Django's built-in
`loaddata` command under the hood. Unlike `loaddata`, `load_fixtures` allows you
to load multiple fixtures without passing their labels to the command. The only
thing you need to do is to configure the fixtures to load in the settings.
Ah, yes... and it also allows you to **easily upload media files** (images,
files, etc.) from the fixtures.

## Installation

```bash
pip install django-smart-fixtures
```

Add `django_smart_fixtures` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django_smart_fixtures',
    ...
]
```

## Configuration

Let's say you have the following fixtures:

```plaintext
my_app/
└──fixtures/
    ├── fixtures1.yaml
    ├── fixtures2.yaml
    └── images/
        ├── image1.jpg
        └── image2.jpg
    
my_other_app/
└──fixtures/
    ├── fixtures3.yaml
    └── files/
        ├── file1.txt
        └── file2.txt
```

You can configure the fixtures to load in the settings:

```python
# settings.py
FIXTURES = {
    'labels': [
        'fixtures1',
        'fixtures2',
        'fixtures3',
    ],
    'media': [
        {
            'src': BASE_DIR / 'my_app' / 'fixtures' / 'images',
            'dest': BASE_DIR / 'media' / 'my_app' / 'images',
        },
        {
            'src': BASE_DIR / 'my_other_app' / 'fixtures' / 'files',
            'dest': BASE_DIR / 'media' / 'my_other_app' / 'files',
        },
    ],
}
```

Then you can load all these fixtures by running:

```bash
python manage.py load_fixtures
```

This will load all the fixtures defined in `fixtures1.yaml`, `fixtures2.yaml`,
and `fixtures3.yaml`. It will also copy all files from `images` and `files`
folders to the media folder.

## Defining fixtures with media files

When defining paths to media files in the fixture files, you should use paths
relative to the media root directory. The media root directory is defined by the
`MEDIA_ROOT` setting. The paths should be defined in the following way:

```yaml
- model: my_app.MyModel
  pk: 1
  fields:
    image: my_app/images/image1.jpg
```

Using the above example, files from `images` will end up in the
`media/my_app/images` folder, and files from `files` will end up in the
`media/my_other_app/files` folder. Relative to media root directory, paths of
copied files will be:

- `my_app/images/image1.jpg`
- `my_app/images/image2.jpg`
- `my_other_app/files/file1.txt`
- `my_other_app/files/file2.txt`

The above paths should be used in the fixture files for the `models.ImageField`,
`models.FileField`, and other media related fields.

## YAML fixtures

If you're defining fixtures in YAML files, make sure to use `.yaml` extension
instead of `.yml` for the fixture files because Django's `loaddata` command does
not support `.yml` files.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an
Issue.

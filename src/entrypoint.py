import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

if __name__ == '__main__':
    print('entrypoint')
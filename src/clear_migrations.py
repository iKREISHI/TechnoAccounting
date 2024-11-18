import os
import django
from django.core.management import call_command


def clear_migrations():
    # Указываем базовую директорию проекта
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Проходим по всем приложениям в проекте
    for root, dirs, files in os.walk(base_dir):
        if "migrations" in dirs:
            migrations_dir = os.path.join(root, "migrations")

            # Удаляем все файлы миграций, кроме __init__.py
            for file in os.listdir(migrations_dir):
                if file != "__init__.py" and file.endswith(".py"):
                    os.remove(os.path.join(migrations_dir, file))
                    print(f"Удален: {os.path.join(migrations_dir, file)}")

            print(f"Очищена папка миграций: {migrations_dir}")

    # Очищаем таблицу django_migrations в базе данных
    print("Очистка таблицы миграций в базе данных...")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
    django.setup()
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations")
    except Exception as e:
        print(f'Error: {e}')
    print("Таблица django_migrations очищена.")

    # Создаем новые пустые миграции
    # print("Создаем новые пустые миграции...")
    # call_command("makemigrations")


if __name__ == "__main__":
    clear_migrations()

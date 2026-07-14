"""
Самостоятельный скрипт для заполнения БД корзин (Cart/CartItem) реалистичными
тестовыми данными. Не требует management-команды.

Куда положить:
    Можно оставить в корне проекта (там же, где находится папка marketplace_cart
    с manage.py внутри) — путь определяется автоматически, переносить не нужно.

Запуск (из любой директории):
    python main.py
    python main.py --users 20
    python main.py --items-per-cart-min 1 --items-per-cart-max 5
    python main.py --product-id-min 1 --product-id-max 200
    python main.py --flush
"""

import argparse
import os
import random
import sys
from pathlib import Path

# --- Настройка Django ---
SCRIPT_DIR = Path(__file__).resolve().parent

_candidates = [
    SCRIPT_DIR,                       # main.py лежит рядом с manage.py
    SCRIPT_DIR / 'marketplace_cart',  # main.py лежит на уровень выше
]
PROJECT_DIR = next((c for c in _candidates if (c / 'manage.py').exists()), SCRIPT_DIR)
sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace_cart.settings')

import django
django.setup()

from django.db import transaction

from marketplace_cart_app.models import Cart, CartItem


@transaction.atomic
def seed(users_count, min_items, max_items, product_id_min, product_id_max, flush):
    if flush:
        print('Удаляю существующие данные...')
        CartItem.objects.all().delete()
        Cart.objects.all().delete()

    print('Создаю корзины...')
    created_carts = 0
    created_items = 0

    existing_users = set(Cart.objects.values_list('user', flat=True))

    for user_id in range(1, users_count + 1):
        if user_id in existing_users:
            cart = Cart.objects.get(user=user_id)
        else:
            cart = Cart.objects.create(user=user_id)
            created_carts += 1

        # не у всех пользователей есть товары в корзине — реалистичнее
        if random.random() < 0.15:
            continue

        items_count = random.randint(min_items, max_items)
        used_products_in_cart = set()

        for _ in range(items_count):
            product_id = random.randint(product_id_min, product_id_max)
            # избегаем дублей одного товара в одной корзине
            attempts = 0
            while product_id in used_products_in_cart and attempts < 10:
                product_id = random.randint(product_id_min, product_id_max)
                attempts += 1
            used_products_in_cart.add(product_id)

            CartItem.objects.create(
                cart=cart,
                product=product_id,
                quantity=random.randint(1, 5),
            )
            created_items += 1

    print(f'  Корзин создано: {created_carts}')
    print(f'  Товаров в корзинах создано: {created_items}')
    print('Заполнение базы данных завершено успешно!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Заполнение БД корзин тестовыми данными')
    parser.add_argument('--users', type=int, default=20, help='Количество пользователей/корзин')
    parser.add_argument('--items-per-cart-min', type=int, default=1)
    parser.add_argument('--items-per-cart-max', type=int, default=5)
    parser.add_argument('--product-id-min', type=int, default=1,
                         help='Минимальный ID товара (из marketplace_product)')
    parser.add_argument('--product-id-max', type=int, default=200,
                         help='Максимальный ID товара (из marketplace_product)')
    parser.add_argument('--flush', action='store_true')
    args = parser.parse_args()

    seed(
        users_count=args.users,
        min_items=args.items_per_cart_min,
        max_items=args.items_per_cart_max,
        product_id_min=args.product_id_min,
        product_id_max=args.product_id_max,
        flush=args.flush,
    )
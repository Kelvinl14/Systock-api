# from faker import Faker
# from sqlalchemy.orm import Session
# from db.database import SessionLocal
# from models import Category, Product, Store, Supplier
# import random
#
# fake = Faker("pt_BR")
#
# db: Session = SessionLocal()
#
# def create_categories(n=10):
#     categories = []
#     for _ in range(n):
#         cat = Category(
#             name=fake.word().capitalize(),
#             description=fake.sentence()
#         )
#         db.add(cat)
#         categories.append(cat)
#     db.commit()
#     return categories
#
# def create_suppliers(n=10):
#     suppliers = []
#     for _ in range(n):
#         s = Supplier(
#             name=fake.company(),
#             email=fake.company_email(),
#             phone=fake.phone_number(),
#         )
#         db.add(s)
#         suppliers.append(s)
#     db.commit()
#     return suppliers
#
# def create_products(categories, n=50):
#     products = []
#     for _ in range(n):
#         p = Product(
#             name=fake.word().capitalize() + " " + fake.word().capitalize(),
#             description=fake.sentence(),
#             cost_price=round(random.uniform(10, 200), 2),
#             sale_price=round(random.uniform(50, 500), 2),
#             category_id=random.choice(categories).id,
#             active=True,
#         )
#         db.add(p)
#         products.append(p)
#     db.commit()
#     return products
#
# def create_stores():
#     store = Store(
#         name="Estoque Central",
#         address=fake.address(),
#         phone=fake.phone_number()
#     )
#     db.add(store)
#     db.commit()
#     return store
#
# def run_seed():
#     print("Criando seed de dados...")
#
#     store = create_stores()
#     categories = create_categories()
#     suppliers = create_suppliers()
#     products = create_products(categories)
#
#     print("Seed concluído com sucesso!")
#
# if __name__ == "__main__":
#     run_seed()
from faker import Faker
from random import uniform

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.category import Category
from app.models.product import Product

fake = Faker("pt_BR")


def create_categories(db: Session, n=8):
    categories = []

    for _ in range(n):
        cat = Category(
            name=fake.unique.word().capitalize(),
            description=fake.sentence(nb_words=8)
        )
        db.add(cat)
        categories.append(cat)

    db.commit()
    return categories


def create_products(db: Session, categories, n=40):
    products = []

    for _ in range(n):
        category = fake.random_element(categories)

        product = Product(
            name=fake.unique.word().capitalize() + " " + fake.word().capitalize(),
            description=fake.sentence(nb_words=12),
            cost_price=round(uniform(10, 200), 2),
            sale_price=round(uniform(50, 600), 2),
            date_added=fake.date_between(start_date='-60d', end_date='today'),
            active=False,
            category_id=category.id
        )

        db.add(product)
        products.append(product)

    db.commit()
    return products


def run_seed():
    db: Session = SessionLocal()
    print("🔄 Gerando seed de categorias e produtos...\n")

    # 1. Criar categorias
    categories = create_categories(db)
    print(f"✔ {len(categories)} categorias criadas.")

    # 2. Criar produtos relacionados às categorias
    products = create_products(db, categories)
    print(f"✔ {len(products)} produtos criados.\n")

    print("🎉 Seed concluído com sucesso!")


if __name__ == "__main__":
    run_seed()

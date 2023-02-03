from django.core.management.base import BaseCommand
import csv
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Loads data from data/ingredients.csv"

    def handle(self, *args, **options):
        print("====== Loading data... =====")
        with open('data/ingredients.csv', newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            for row in data:
                category, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
                if created:
                    print(f'Ingredient {category.name} created')
                else:
                    print(f'Ingredient {category.name} exists.')
        print('===== Ingredients uploaded =====')

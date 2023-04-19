import csv
import os
from typing import Type, Union

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import ForeignKey, Model
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class Command(BaseCommand):
    """Import data from .csv files to DB."""

    help: str = 'Fill the DB whith record values from .csv files'
    csv_path: str = os.path.join(settings.BASE_DIR, 'static/data')
    csvf_model: dict[str, Type[Model]] = {
        "users.csv": User,
        "category.csv": Category,
        "genre.csv": Genre,
        "titles.csv": Title,
        "genre_title.csv": GenreTitle,
        "review.csv": Review,
        "comments.csv": Comment,
    }

    @staticmethod
    def rel_id_to_model_inst(
            model: Type[Model],
            row: dict[str, Union[int, str, None]]) -> None:
        """Substitutes the instance of the associated
        model instead of the id."""
        for field in model._meta.fields:
            if isinstance(field, ForeignKey):
                if field.name in row:
                    if not row[field.name]:
                        continue
                    related_model = field.remote_field.model
                    obj = related_model.objects.get(id=row[field.name])
                    row[field.name] = obj
                else:
                    raise CommandError(f"Can't find {field.name=} "
                                       f"of model {model} in csv file")

    def create_model_instances(self, csv_f: str, model: Type[Model]) -> None:
        """Create model instances."""
        records: list = []
        file: str = os.path.join(self.csv_path, csv_f)
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.rel_id_to_model_inst(model, row)
                record = model(**row)
                records.append(record)
        try:
            model.objects.bulk_create(records)
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(
                f'Error importing {model} records. {e}'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Importing {model} records completed successfully.'))

    def add_arguments(self, parser):
        parser.add_argument(
            '-d'
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=False,
            help='Delete existing records before generating new ones',
        )

    def handle(self, *args, **options):
        if options["delete_existing"]:
            try:
                [model.objects.all().delete() for model
                 in reversed(self.csvf_model.values())]
            except ProtectedError as e:
                self.stdout.write(self.style.ERROR(
                    f'Error while deleting instances. {e}'))
            else:
                self.stdout.write(
                    self.style.SUCCESS('All existing records deleted'))
        for csvf, model in self.csvf_model.items():
            self.create_model_instances(csvf, model)
        self.stdout.write(self.style.SUCCESS('All models records saved'))

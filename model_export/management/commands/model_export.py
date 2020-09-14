import csv
import os
import types
from itertools import zip_longest

import django
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        consistency_check_labels = {config.label for config in apps.get_app_configs()}
        for app_label in consistency_check_labels:
            for model in apps.get_app_config(app_label).get_models():
                self.export_csv_columns(model)

        print("CSVへのエクスポートが完了しました")

    def export_csv_columns(self, model):
        file_path = "table_design_csv/" + model.__module__.split('.')[0] + '/' + model.__name__ + ".csv"
        os.makedirs("table_design_csv/" + model.__module__.split('.')[0] + '/', exist_ok=True)

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            fields = [field for field in model._meta.fields]

            header = [
                field.db_column if field.db_column is not None else field.name for field in fields
            ]
            header.insert(0, '物理名')

            header_verbose_name = [field.verbose_name for field in fields]
            header_verbose_name.insert(0, '論理名')

            column_type = [field.__class__.__name__ for field in fields]
            column_type.insert(0, 'データタイプ')

            is_primary = ['◯' if field.primary_key else '' for field in fields]
            is_primary.insert(0, 'PK')

            unique_columns = []
            for unique_together in model._meta.unique_together:
                is_unique = ['◯' if field.name in unique_together else '' for field in fields]
                is_unique.insert(0, 'UK')
                unique_columns.append(is_unique)

            is_foreign = [
                field.target_field.model.__name__ + '.' + field.target_field.column if field.__class__ is django.db.models.fields.related.ForeignKey else ''
                for field in fields]
            is_foreign.insert(0, 'FK')

            is_default = [field.default.__name__ if isinstance(field.default, types.FunctionType) else field.default if field.default is not django.db.models.fields.NOT_PROVIDED else ''
                          for field
                          in fields]

            is_default.insert(0, 'デフォルト')

            is_blank = ['◯' if field.blank else '' for field in fields]
            is_blank.insert(0, '空白OKか')

            is_null = ['◯' if field.null else '' for field in fields]
            is_null.insert(0, 'nullOKか')

            is_choices = [field.choices if field.choices else '' for field in fields]
            is_choices.insert(0, 'Enum値')

            is_max_length = [field.max_length for field in fields]
            is_max_length.insert(0, '最大文字列')

            is_auto_now = ['◯' if field.__class__ is django.db.models.fields.DateTimeField else '' for field in
                           fields]
            is_auto_now.insert(0, 'auto_now(保存時の時間を自動入力)')

            d = [header, header_verbose_name, column_type, is_primary, *unique_columns, is_foreign,is_default,
                             is_blank, is_null, is_choices, is_max_length, is_auto_now]
            export_data = zip_longest(*d, fillvalue='')

            writer.writerows(export_data)
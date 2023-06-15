from django.core.management.base import BaseCommand
import pandas
import sqlite3

from django import db

import_template = [
    ("category", "reviews_category", {}, [], []),
    (
        "comments",
        "reviews_comments",
        {
            "review_id": "review_id_id",
            "author": "author_id",
        },
        [],
        [],
    ),
    ("genre_title", "reviews_titles_genre", {"title_id": "titles_id"}, [], []),
    ("genre", "reviews_genre", {}, [], []),
    (
        "review",
        "reviews_review",
        {
            "title_id": "title_id_id",
            "author": "author_id",
        },
        [],
        [],
    ),
    (
        "titles",
        "reviews_titles",
        {"category": "category_id"},
        [],
        [("year", "%Y")],
    ),
    (
        "users",
        "reviews_user",
        {},
        [
            ("password", "change_me"),
            ("last_login", "2023-06-15 06:02:58.522746"),
            ("is_superuser", False),
            ("is_staff", False),
            ("is_active", False),
            ("date_joined", "2023-06-15 06:02:58.522746"),
            ("confirmation_code", "default"),
        ],
        [],
    ),
]

class Command(BaseCommand):
    help = 'Import data from local csv files into database.'

    def handle(self, *args, **kwargs):

        db_path = db.utils.settings.DATABASES['default']['NAME']
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        for entry in import_template:
            file_name = entry[0]
            table_name = entry[1]
            columns_to_rename = entry[2]
            columns_to_add = entry[3]
            columns_date_modification_type = entry[4]

            c.execute(
                f"DELETE FROM {table_name};",
            )

            conn.commit()

            # давайте предположим, что файлы будут всегда лежать здесь
            df = pandas.read_csv(f"static/data/{file_name}.csv")

            df.rename(columns=columns_to_rename, inplace=True)

            if columns_to_add:
                for column in columns_to_add:
                    name = column[0]
                    default_value = column[1]
                    df.insert(0, name, default_value)

            if columns_date_modification_type:
                for column in columns_date_modification_type:
                    name = column[0]
                    format = column[1]
                    df[name] = pandas.to_datetime(df[name], format=format)

            df.to_sql(table_name, conn, if_exists="append", index=False)

        conn.close()

        self.stdout.write("Import Complete!")

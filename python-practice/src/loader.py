import json
from datetime import datetime
from pathlib import Path

import psycopg


class DataLoader:
    def __init__(self, connection: psycopg.Connection):
        self._connection = connection

    @staticmethod
    def _read_json(file_path: Path) -> list[dict]:
        with file_path.open("r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError(f"Expected a JSON array in file {file_path}")

        return records

    def load_rooms(self, file_path: Path) -> int:
        rooms = self._read_json(file_path)
        rows = [(room["id"], room["name"]) for room in rooms]

        query = """
            INSERT INTO rooms (id, name)
            VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE
            SET name = EXCLUDED.name
        """

        with self._connection.cursor() as cursor:
            cursor.executemany(query, rows)

        return len(rows)

    def load_students(self, file_path: Path) -> int:
        students = self._read_json(file_path)
        rows = [
            (
                student["id"],
                student["name"],
                datetime.fromisoformat(student["birthday"]).date(),
                student["sex"],
                student["room"],
            )
            for student in students
        ]

        query = """
            INSERT INTO students (id, name, birthday, sex, room)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET name = EXCLUDED.name,
                birthday = EXCLUDED.birthday,
                sex = EXCLUDED.sex,
                room = EXCLUDED.room
        """

        with self._connection.cursor() as cursor:
            cursor.executemany(query, rows)

        return len(rows)

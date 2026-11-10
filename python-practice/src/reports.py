import psycopg
from psycopg.rows import dict_row


class ReportRepository:
    def __init__(self, connection: psycopg.Connection):
        self._connection = connection

    def get_student_counts(self) -> list[dict]:
        query = """
            SELECT r.id, r.name,  COUNT(s.id) AS students_count
            FROM rooms AS r
            LEFT JOIN students AS s
            ON r.id = s.room
            GROUP BY r.id, r.name;
        """

        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_avg_age(self) -> list[dict]:
        query = """
            SELECT r.id, r.name, AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) AS avg_age
            FROM rooms AS r
            JOIN students AS s
            ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY avg_age, r.id
            LIMIT 5;
        """

        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_diff_age(self) -> list[dict]:
        query = """
            SELECT r.id,
            r.name,
            MAX(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) - 
            MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) AS age_diff
            FROM rooms AS r
            JOIN students AS s
            ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY age_diff DESC, r.id
            LIMIT 5;
        """

        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_diff_sex(self) -> list[dict]:
        query = """
            SELECT r.id, r.name
            FROM rooms AS r 
            JOIN students AS s
            ON r.id = s.room
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT s.sex) > 1
            ORDER BY r.id;
        """

        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

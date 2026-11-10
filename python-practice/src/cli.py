import argparse
from pathlib import Path

import psycopg
from src.database import Database
from src.exporters import JsonExporter, XmlExporter
from src.loader import DataLoader
from src.reports import ReportRepository


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--students", required=True, type=Path)
    parser.add_argument("--rooms", required=True, type=Path)
    parser.add_argument(
        "--format",
        choices=("json", "xml"),
        default="json",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    exporter = JsonExporter()
    exporters = {
        "json": JsonExporter(),
        "xml": XmlExporter(),
    }

    exporter = exporters[args.format]

    with Database().connect() as connection:
        connection.autocommit = True
        loader = DataLoader(connection)
        reports = ReportRepository(connection)

        report_methods = {
            "2": reports.get_student_counts,
            "3": reports.get_avg_age,
            "4": reports.get_diff_age,
            "5": reports.get_diff_sex,
        }

        print("""
            1 — Load data
            2 — Student counts
            3 — Smallest average age
            4 — Largest age difference
            5 — Mixed-sex rooms
            0 — Exit

            Enter one or more actions separated by spaces.
            """)

        while True:
            try:
                actions = input("Actions: ").split()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if actions == ["0"]:
                break

            valid_actions = {"1", *report_methods}

            if any(action not in valid_actions for action in actions):
                print("Unknown action. Use 1–5, or 0 to exit.")
                continue

            for action in actions:
                try:
                    with connection.transaction():
                        if action == "1":
                            rooms_count = loader.load_rooms(args.rooms)
                            students_count = loader.load_students(
                                args.students
                            )
                        else:
                            result = report_methods[action]()

                    if action == "1":
                        print(f"Rooms processed: {rooms_count}")
                        print(f"Students processed: {students_count}")
                    else:
                        output_dir = Path(__file__).resolve().parents[1] / "output"
                        file_path = output_dir / f"report_{action}.{args.format}"
                        exporter.export(result, file_path)
                        print(f"Report saved: {file_path}")

                except (psycopg.Error, OSError, ValueError, KeyError) as error:
                    print(f"Action {action} failed: {error}")
     

if __name__ == "__main__":
    main()

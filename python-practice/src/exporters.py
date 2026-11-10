import json
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path


class JsonExporter:
    def export(self, rows: list[dict], file_path: Path) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(
                rows,
                file,
                ensure_ascii=False,
                indent=2,
                default=self._serialize,
            )

    @staticmethod
    def _serialize(value):
        if isinstance(value, Decimal):
            return float(value)

        raise TypeError(
            f"Cannot serialize {type(value).__name__} to JSON"
        )

class XmlExporter:
    def export(self, rows: list[dict], file_path: Path) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        root = ET.Element("report")

        for row in rows:
            room = ET.SubElement(root, "room")

            for key, value in row.items():
                field = ET.SubElement(room, key)

                if value is None:
                    field.set("null", "true")
                else:
                    field.text = str(value)

        ET.indent(root, space="  ")

        tree = ET.ElementTree(root)
        tree.write(
            file_path,
            encoding="utf-8",
            xml_declaration=True,
        )
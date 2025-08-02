import json
import csv

INPUT_PATH = "../data/fewshot_dataset/desc02.json"
OUTPUT_PATH = "../data/fewshot_dataset/file02.csv"

def extract_property_text(property_sets):
    props = []
    for pset in property_sets:
        for prop in pset.get("Properties", []):
            name = prop.get("Name", "").strip()
            value = prop.get("Value", "").strip()
            if name and value:
                props.append(f"{name}: {value}")
    return "; ".join(props)

def is_allowed_classification(system):
    if not system:
        return False
    system_lower = system.lower()
    return "cci" in system_lower or "uniclass" in system_lower

def parse_objects(data):
    parsed_rows = []

    for obj in data:
        attributes = {attr["Name"]: attr["Value"] for attr in obj.get("Attributes", [])}
        property_sets = obj.get("PropertySets", [])
        classifications = obj.get("Classifications", [])

        guid = attributes.get("Guid", "")
        ifc_type = attributes.get("IfcEntity", "")
        name = attributes.get("Name", "")

        # Budujemy pełny opis tekstowy
        text_parts = []
        if name:
            text_parts.append(name)
        property_text = extract_property_text(property_sets)
        if property_text:
            text_parts.append(property_text)
        full_text = " — ".join(text_parts)

        # Klasyfikacje
        for cls in classifications:
            system = cls.get("System", "")
            code = cls.get("Code", "")
            if is_allowed_classification(system) and code:
                parsed_rows.append({
                    "GlobalId": guid,
                    "IfcType": ifc_type,
                    "Name": name,
                    "Text": full_text,
                    "ClassificationSystem": system,
                    "ClassificationCode": code
                })

    return parsed_rows

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    parsed = parse_objects(data)

    if not parsed:
        print("Nie znaleziono żadnych obiektów z klasyfikacjami CCI/Uniclass.")
        return

    # Zapis do CSV
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["GlobalId", "IfcType", "Name", "Text", "ClassificationSystem", "ClassificationCode"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed)

    print(f"Zapisano {len(parsed)} wierszy do {OUTPUT_PATH}")

if __name__ == "__main__":
    main()

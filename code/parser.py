import json

def parse_ifc_object(obj):
    attrs = {att['Name']: att['Value'] for att in obj.get('Attributes', [])}
    props = []

    for pset in obj.get('PropertySets', []):
        for prop in pset.get('Properties', []):
            name = prop.get('Name', '')
            value = prop.get('Value', '')
            unit = prop.get('Unit', '')
            if value:
                props.append(f"{name}: {value} {unit}".strip())

    parts = [
        f"Typ IFC: {attrs.get('IfcEntity', 'Unknown')}",
        f"Nazwa: {attrs.get('Name', '')}",
        f"Opis: {attrs.get('Description', '')}",
    ]

    if props:
        parts.append("Właściwości: " + "; ".join(props))

    return " | ".join(parts)

# Wczytanie pliku JSON
with open("sample_ifc.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Przetworzenie do listy opisów
parsed_descriptions = [parse_ifc_object(obj) for obj in data]

# Podgląd
for desc in parsed_descriptions[:5]:
    print(desc)
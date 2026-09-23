import csv
import os

def apartment_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'apartments_data.csv')
    data = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                data.append({
                    "type": row["Type"],
                    "name": row["Name"],
                    "lat": float(row["Latitude"]),
                    "lng": float(row["Longitude"]),
                    "images": row["Images"].split(','),
                    "address": row["Address"],
                    "labels1": row["Labels1"].split(','),
                    "price1": list(map(float, row["Price1"].split(','))),
                    "labels2": row["Labels2"].split(','),
                    "price2": list(map(float, row["Price2"].split(','))),
                    "labels3": row["Labels3"].split(','),
                    "price3": list(map(float, row["Price3"].split(','))),
                })
            except Exception as e:
                print(f"[ERROR] CSV row error: {e}")
                continue

    return data

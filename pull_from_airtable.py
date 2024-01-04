import requests
import csv
from datetime import datetime

from configuration import airtable_token, base_id, table_id

url2 = f"https://api.airtable.com/v0/{base_id}/{table_id}"
headers = {
    "Authorization": "Bearer " + str(airtable_token),
    "Content-Type": "application/json",
}
current_datetime = datetime.now()
timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
response = requests.get(url2, headers=headers)
print("Export start")

if response.status_code == 200:
    data = response.json()['records']
    print(f"Record count: {len(data)}")  # Print the count of records

    # Writing data to CSV
    with open(timestamp + 'airtable_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # Assuming all records have the same fields, use the first record to write column headers
        if data:
            headers = data[0]['fields'].keys()
            writer.writerow(headers)

            # Writing the data of each record
            for skunk in data:
                print(skunk)
                writer.writerow(skunk['fields'].values())
else:
    print("Failed to retrieve data")

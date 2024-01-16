#Requirements to turn NIH XML into CSV
import json
import xmltodict
import csv
import requests
from datetime import datetime

# Specify the URL for the XML file
xml_url = 'https://www.techtransfer.nih.gov/sites/default/files/nih-abstracts.xml'

# Specify the local XML file path
local_xml_file_path = 'nih-abstracts.xml'

# Fetch XML data from the URL and save it locally
response = requests.get(xml_url)
with open(local_xml_file_path, 'wb') as xml_file:
    xml_file.write(response.content)

print("XML File downloaded successfully!")

#Open the file and turn it into a python dictionary
with open("nih-abstracts.xml") as xml_file:
    nih_dict = xmltodict.parse(xml_file.read())
    
#Take full dict output and just get the list you want to loop through
nih_dict_list = nih_dict['marketingProjectList']['marketingProject']

print("File converted to python dictionary object successfully!")

# Generate timestamp for the CSV file name
timestamp = datetime.now().strftime("%Y%m%d")

# Specify the CSV file path with timestamp
csv_file_path = f'NIH_{timestamp}.csv'

# Specify the fields to include in the CSV
fields_to_include = [
    'id', 'title', 'categories', 'abstract', 'collaborativeResearchOpportunity',
    'dateCreated', 'dateUpdated', 'datePublished', 'keywords', 'developmentStageDesc',
    'projectType', 'relatedTechnologiesList', 'inventorList', 'inventorLeadList',
    'licensingContactList', 'technologyList', 'techid', 'techStatus', 'owners'
]

# Extract the header from the first dictionary
header = fields_to_include

# Write data to CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields_to_include)
    
    # Write the header
    writer.writeheader()
    
    # Write the data
    for entry in nih_dict_list:
        # Extract only the selected fields from the dictionary
        filtered_entry = {field: entry.get(field, '') for field in fields_to_include}
        writer.writerow(filtered_entry)
        

print(f'CSV file "{csv_file_path}" has been created.')

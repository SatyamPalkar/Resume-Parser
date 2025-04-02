import requests

url = 'http://localhost:8000/parse_resume/'
file_path = r"C:\Users\satya\OneDrive\Desktop\Jobs\Data Analyst\Satyam_Palkar_Data_Analyst.pdf"

with open(file_path, 'rb') as file:
    response = requests.post(url, files={'file': file})

# Debug the actual response content
print("Status code:", response.status_code)
print("Response content:", response.text)

import requests

response = requests.get('https://www.google.com.mx')   # I/O - bound
items = response.headers.items()                       # CPU - bound
headers = [f'{key}:{value}' for key, value in items]   # CPU - bound
str_headers = "\n".join(headers)                       # CPU - bound
with open('headers_dump.txt', 'w') as ptr_file:        # I/O - bound
    ptr_file.write(str_headers)                        # I/O - bound
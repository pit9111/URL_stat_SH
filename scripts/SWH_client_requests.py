import requests
import json
from requests.exceptions import RequestException, Timeout, ConnectionError

# Load token from environment variable or file
def url_swhid_finder(url):
    SWH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhMTMxYTQ1My1hM2IyLTQwMTUtODQ2Ny05MzAyZjk3MTFkOGEifQ.eyJpYXQiOjE3Mzg2ODM0NTQsImp0aSI6IjhjMGE3YmYyLTZkMGEtNGIxOS04MDcwLWJiNzVkZTVjY2RjNyIsImlzcyI6Imh0dHBzOi8vYXV0aC5zb2Z0d2FyZWhlcml0YWdlLm9yZy9hdXRoL3JlYWxtcy9Tb2Z0d2FyZUhlcml0YWdlIiwiYXVkIjoiaHR0cHM6Ly9hdXRoLnNvZnR3YXJlaGVyaXRhZ2Uub3JnL2F1dGgvcmVhbG1zL1NvZnR3YXJlSGVyaXRhZ2UiLCJzdWIiOiI4MWMwZjNhMS02MGY2LTQyMjQtOGRlNi1jMDViYzAxYjViNjAiLCJ0eXAiOiJPZmZsaW5lIiwiYXpwIjoic3doLXdlYiIsInNlc3Npb25fc3RhdGUiOiJmMzUyNDA0Yi1lMDEwLTQ3NWQtYTQ4NC05Y2M0MDlkYmJlYWYiLCJzY29wZSI6Im9wZW5pZCBvZmZsaW5lX2FjY2VzcyBwcm9maWxlIGVtYWlsIn0.83TRysAPy1XgxaMJjU11Ru5TreOHlloga_sXvvevhMo"  # Replace with your actual token

    headers = {
        "Authorization": f"Bearer {SWH_TOKEN}"
    }

    url = "https://archive.softwareheritage.org/api/1/origin/" + url + "/get/"
    # Make the authenticated request
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        found = resp.json()
        print(found)
        try:
            if found['exception'] == "NotFoundExc":
                return "Resource not found"
        except KeyError:
            try:
                if found['error'] == 'Resource not found':
                    return "Wrong format of URL"
            except KeyError:
                return (found)

    except Timeout as e:
        return f"Request timed out: {e}"

    except ConnectionError as e:
        return f"Connection error: {e}"

    except RequestException as e:
        return f"Request error: {e}"


import requests

url = "https://api.themoviedb.org/3/authentication"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZWM4ZjY0MWU4ZmVmMzA4ZDViMDFhYzI1NjNkNWIyMiIsIm5iZiI6MTczMjgzODQzNC4yOTMzMTQyLCJzdWIiOiI1OTcyN2Y2NjkyNTE0MTdmYTYwMTkxMzkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.hFdmRBamFH50e1eKsCbsxEXGOy13eJJdpWiwb7HQcag"
}

response = requests.get(url, headers=headers)

print(response.text)
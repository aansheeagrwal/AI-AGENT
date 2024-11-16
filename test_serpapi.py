from serpapi.google_search import GoogleSearch



params = {
    "q": "OpenAI",
    "api_key": "49ee4322ad5c1c6f2b926ee7a82e3cc9723e9aafc17fd62fdd779ece88a6b044"
}

search = GoogleSearch(params)
results = search.get_dict()
print(results)




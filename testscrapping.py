import requests

# Cookies convertidos para dict
cookies = {
    "ps_n": "1",
    "datr": "jKgRaOOHaO1AbjJoJmjqS-b6",
    "ig_nrcb": "1",
    "ds_user_id": "2448742298",
    "csrftoken": "0twLk8Y2ma30MjUph43jCNjONNlzx0TW",
    "ig_did": "E66F2999-9072-407B-8C21-973E8620D5C1",
    "ps_l": "1",
    "wd": "1920x959",
    "mid": "aC5DWgALAAG19ClEEzXuSwjc3X79",
    "sessionid": "2448742298%3Aq96TCvOIQvsBqS%3A21%3AAYeD8P0ChAqO_j_PKagZjJzDnsKiRoiUuPUZv_A7ig",
    "rur": "NHA,2448742298,1779398657:01f78492556a102df1b841ba33e5054f4d76cad58a0aaa49585305dfc62a13c92162ad83"
}

# Cabeçalhos típicos de um navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.instagram.com/",
    "X-CSRFToken": cookies["csrftoken"],
    "X-Requested-With": "XMLHttpRequest"
}

# Usar sessão persistente
session = requests.Session()
session.headers.update(headers)
session.cookies.update(cookies)

# URL de exemplo para buscar usuários
url = "https://www.instagram.com/web/search/topsearch/?context=blended&query=pedro&rank_token=0.3953592318270893&count=10"

response = session.get(url)

print("Status:", response.status_code)
print(response.text)

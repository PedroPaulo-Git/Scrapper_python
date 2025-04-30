import requests

# Função para obter cookies e headers
def get_headers():
    cookies = (
        "ps_n=1; "
        "datr=wGURaERLiN3kuj8Vp7zGYlj3; "
        "ds_user_id=2448742298; "
        "csrftoken=E1JM3J3GU37s9MXW9D0VzRftE9VVBA4y; "
        "ig_did=89ACB30B-7EE1-4240-8322-833E48471829; "
        "ps_l=1; "
        "wd=986x872; "
        "mid=aBFlwAABAAEVMKbVZSkqZlzSY3jZ; "
        "sessionid=2448742298%3Ajsf7diDeyWepOl%3A16%3AAYfA9yxd3_GRunoA2rUrILZta1WrqjwShujSsYMedA; "
        "dpr=2; "
        "rur=NHA\\0542448742298\\0541777507348:01f778aa5b5f2f956c31a08715673a248d0f46dfb453327e0c8d2ee8b2d165db577f3cc9"
    )

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.instagram.com/",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": cookies
    }

    return HEADERS

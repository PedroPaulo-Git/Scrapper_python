# import requests

# # Função para obter cookies e headers
# def get_headers():
#     cookies = (
#         "ps_n=1; "
#         "datr=wGURaERLiN3kuj8Vp7zGYlj3; "
#         "ds_user_id=2448742298; "
#         "csrftoken=E1JM3J3GU37s9MXW9D0VzRftE9VVBA4y; "
#         "ig_did=89ACB30B-7EE1-4240-8322-833E48471829; "
#         "ps_l=1; "
#         "wd=986x872; "
#         "mid=aBFlwAABAAEVMKbVZSkqZlzSY3jZ; "
#         "sessionid=2448742298%3Ajsf7diDeyWepOl%3A16%3AAYfA9yxd3_GRunoA2rUrILZta1WrqjwShujSsYMedA; "
#         "dpr=2; "
#         "rur=NHA\\0542448742298\\0541777507348:01f778aa5b5f2f956c31a08715673a248d0f46dfb453327e0c8d2ee8b2d165db577f3cc9"
#     )

#     HEADERS = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
#         "Referer": "https://www.instagram.com/",
#         "X-Requested-With": "XMLHttpRequest",
#         "Cookie": cookies
#     }

#     return HEADERS
import requests

# Função para obter cookies e headers
def get_headers():
    cookies = (
        "datr=jKgRaOOHaO1AbjJoJmjqS-b6; "
        "ds_user_id=2448742298; "
        "csrftoken=LCwrsTqLWWkZTqgEbAVWeK8luUVx51CM; "
        "ig_did=E66F2999-9072-407B-8C21-973E8620D5C1; "
        "wd=1920x959; "
        "mid=aBGojAABAAHYhyf4JgvIw5kHMFq7; "
        "sessionid=2448742298%3A4eiTQmlAPO0JMI%3A4%3AAYflqvOehAKchlXcV9w_QHcAVFO6E08nD6dpIrCb6w; "
        "dpr=1; "
        "rur=NHA\\0542448742298\\0541777585349:01f7057962eba71c5fb8a098e03405200ac1b90e40217c3e803a9d48afb9d0b823e28ace"
    )

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.instagram.com/",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": cookies
    }

    return HEADERS

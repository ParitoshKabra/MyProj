import requests
clientId = "9iXxR2JLU4HyfCi1umE5nDKTyjbpicWrFFUQPWAV"
secret_token = "NR5elrClc66eM2i8Db8E80cr8FiZyYnUEMsW4Jnvu0Fa4reL0CT36hRBuHI7QcDXx74CrtGQLTcYyA7CizhWabYbuxMPogZ6KUCqlxtVUsmUrHnje5hfQzahMh5nmhYu"

auth_url_token = "https://channeli.in/open_auth/token/"
auth_user_data = "https://channeli.in/open_auth/get_user_data/"

def exchange_code(code : str):
    print(code)
    data = {
        "client_id": clientId,
        "client_secret": secret_token,
        "grant_type": 'authorization_code',
        "redirect_uri": "http://127.0.0.1:8000/trelloAPIs/oauth_redirect",
        "code": code, 
        "scope":"read"
    }
    res = requests.post(auth_url_token,data=data)
    credentials = res.json()
    access_token = credentials["access_token"]
    params = {
        "Authorization": f"Bearer {access_token}"
    }
    res = requests.get(auth_user_data, headers=params)
    user = res.json()
    return user


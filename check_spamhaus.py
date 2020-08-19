import requests


def method1(domain):
    r_auth = requests.get('https://mxtoolbox.com/api/v1/user')
    TempAuthKey = r_auth.json()['TempAuthKey']
    payload = { 
        "accept":"application/json, text/javascript, */*; q=0.01",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type":"application/json; charset=utf-8", 
        "referer":"https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a{}&run=toolpage".format(domain),
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-origin",
        "tempauthorization":TempAuthKey,
        "user-agent":"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
     
    url="https://mxtoolbox.com/api/v1/Lookup?command=blacklist&argument={}&resultIndex=2&disableRhsbl=true&format=2".format(domain)
    r = requests.get(url, headers=payload)
    data = r.json()
    index1 = data['HTML_Value'].find('Spamhaus DBL')
    if 'was listed' in data['HTML_Value'][index1:(index1+150)]:
        return False
    else:
        return True

def method2(domain):
    url = "http://multirbl.valli.org/lookup/"+str(domain)+".html"
    text = requests.get(url).text
    ash = re.findall('"asessionHash": "([^"]+)"', text)[0]
    r2 = requests.get("http://multirbl.valli.org/json-lookup.php?ash="+ash+"&rid=DNSBLBlacklistTest_42&lid=640&q="+domain)
    if '"result":false' in r2.text:
        return False
    else:
        return True

def check_spamhaus(domain):
    """ 
    Return True if domain is good
           False if domain is bad
           None otherwise
    """
    try:
        return method1(domain)
    except:
        pass
    try:
        return method2(domain)
    except:
        pass
    return None




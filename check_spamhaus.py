import requests
import re



def check_spamhaus_method1(domain): 
    token_list = [
        '1d30737e-971f-45a8-af52-40d022c80240',
        '4fd1da4c-76a0-4222-ab98-1890aca21b6e',
        'dab115f4-48c6-4ac8-95fd-72c0ef9f6d25',
        '1379f99e-5556-4ad6-9055-4db63c70463e',
        '49ae5869-59e8-480d-ace5-f92b4a4b8f9a',
        'e49e6bde-76dd-4b8c-9890-d57fa477a41d',
        '73d31052-7997-4a7f-ab9a-308a6769f297',
        'd4994ace-bbfe-404c-89b2-e2e0c6b41176',
        '4874bcf6-0fcf-4963-a2c5-69c11bddc00b',
        '9f7b4a05-df48-47ba-b10c-f62992ef56ef',
    ]
    import random
    random.shuffle(token_list)
    for token in token_list:
        print('[check_spamhaus_method1] use token %s' % token)
        url = 'https://api.mxtoolbox.com/api/v1/Lookup/blacklist/?argument={domain}&Authorization={token}'
        url = url.format(domain=domain, token=token)
        r = requests.get(url)
        print('[check_spamhaus_method1] status code: %s' % r.status_code)
        if r.status_code < 300:
            for x in r.json()['Failed']:
                if 'spamhaus dbl' in x['Name'].lower():
                    print('bad')
                    return False 
            print('good')
            return True
    return None


def check_spamhaus_method2(domain):
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
    print('Check Spamhaus for: %s' % domain)
    try:
        c1 = check_spamhaus_method1(domain)
        if c1 != None:
               return c1
    except Exception as e:
        print('ERR check_spamhaus_method1: %s' % e)
    try:
        return check_spamhaus_method2(domain)
    except Exception as e:
        print('ERR check_spamhaus_method2: %s' % e)
    return None




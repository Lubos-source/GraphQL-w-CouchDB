import urllib.request, json 
from urllib.parse import urlencode
from base64 import b64encode
import getpass
from platform import python_version

print(python_version())
serverAddress = 'http://127.0.0.1:31111/'
userName = "admin"
password = "admin"

def printJson(jsondata):
    result = json.dumps(jsondata, indent=4)
    print(result)
    #return result

cookie = ''    
def couchDbLogin(user = userName, password = password):
    global cookie

    url = serverAddress + '_session'
    data = {'username' : user, 'password': password}

    data = urllib.parse.urlencode(data).encode()
    request = urllib.request.Request(url, data = data, method = 'POST')
    response = urllib.request.urlopen(request)
    cookie = response.headers['Set-Cookie']
    cookie = cookie.split(';')[0]

    result = response.read()
    #result = response.read().decode('utf8')
    return result
    
def couchDbAPICall(location, method = 'GET', data = None):
    global cookie
    url = serverAddress + location
    encdata = None
    if not(data == None):
        encdata = json.dumps(data).encode('utf8')
        print(encdata)
    request = urllib.request.Request(url, data = encdata, method = method)
    request.add_header('Cookie', cookie)   
    result = '{}'
    print(request)

    if not(data == None):
        request.add_header('Content-Type', 'application/json')   
    try:
        response = urllib.request.urlopen(request)
        result = response.read()
    except urllib.error.HTTPError as err:
        print(err)
        print(err.reason)
        print(err.headers)
        result = err.read()
        #response = err.response
    
    #result = response.read().decode('utf8')
    return json.loads(result)

couchDbLogin()
printJson(couchDbAPICall(location = ''))


data = couchDbAPICall('_session', 'GET')
print('_session')
printJson(data)
dbs = couchDbAPICall('_all_dbs', 'GET')
print('_all_dbs')
printJson(dbs)
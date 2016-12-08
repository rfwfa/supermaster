import requests, json

def getHttpResponse(url, http_method, parameters):
    try:
        if http_method == 'POST':
            method = requests.post
        elif http_method == 'GET':
            method = requests.get
        elif http_method == 'HEAD':
            method = requests.head
        elif http_method == 'DELETE':
            method = requests.delete
        elif http_method == 'OPTIONS':
            method = requests.options
        else:
            return -1
        response = method(url, params=parameters)
        return response
    except Exception as e:
        print e
        return -1
        
        
resp = getHttpResponse('https://echo.getpostman.com/post', 'GET', {'username':'admin','password':'pass'})
print resp
if resp.content != '':
    print(json.loads(resp.content))

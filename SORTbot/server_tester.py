import json
import urllib.request

def post_request(output, location):
    myurl = location

    print("Initialising request")

    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')

    print("Getting the JSON ready")

    jsondata = json.dumps(output)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))

    #print("The JSON data is: ", jsondataasbytes)

    print("Sending the request")

    response = urllib.request.urlopen(req, jsondataasbytes)

    print("The result is: ")
    bytes_data = response.read()

    print(bytes_data.decode("utf-8"))

def test_signin():

    print("testing SIGNIN")
    output = dict()
    output['username'] = 'octa'
    output['password'] = '1234'
    post_request(output, "http://localhost:5000/signin")

def test_signup():
    print('testing SINGUP')
    output = dict()
    output['username'] = 'octa'
    output['password'] = '1234'
    output['first_name'] = 'Octavian'
    output['last_name'] = 'Rosu'
    output['email'] = 'tma33@cam.ac.uk'
    post_request(output, "http://localhost:5000/signup")

def test_add_entry():
    print('testing ADD-ENTRY')
    output = dict()
    output['userID'] = 1
    output['itemID'] = 2
    post_request(output, "http://localhost:5000/add-entry")

def test_get_info():
    print('testing ADD-ENTRY')
    output = dict()
    output['userID'] = 1
    post_request(output, "http://localhost:5000/get-information")

if __name__ == "__main__":
    test_signin()
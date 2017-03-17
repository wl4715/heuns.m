from flask import Flask, request, jsonify, Response
from DatabaseHandler import DatabaseHandler as Dh

app = Flask(__name__)

dh = Dh()

@app.route("/get-information", methods=["POST"])
def get_info():
    """
        A method that returns the general information for a specific user

        It expects a HTTP POST request containing a JSON of the format:
        {
            "userID": <userID>
        }
    :return:
        A JSON with the following format:
        {
            "first_name": <first_name>          - first name of the user
            "last_name": <last_name>            - last name of the user
            "points": {
                "total": <total>                - the total number of points of the entry
                "last":  <last>                 - the last point earned
            }
            "history": [                         -- it is a list of the most recent entries (up to 10)
                {
                    "item": <item>              - the name of the item
                    "date": <date>              - the date it was added
                    "points": <points>          - the points the user got for that item
                }
            ]
        }

    """
    print("Got a GET-INFO request")
    if request.is_json:
        data = request.json
        if (len(data) == 1) and ('userID' in data):
            result = dh.get_general_data(userID=data['userID'])
            return jsonify(result)
        else:
            print("Wrong JSON")
            return Response(response="Wrong JSON format", status=400)
    else:
        print("not JSON")
        return Response(response="Expected JSON", status=400)


@app.route("/add-entry", methods=["POST"])
def add_entry():
    """
        Method that adds an entry to our database

        It expects a HTTP POST request containing a JSON of the format:
        {
            "userID": <userid>      -- the id of the user
            "itemID": <itemID>      -- the id of the item we want to insert
        }
    :return:
        A JSON representing the result of the query:
        {
            "success": True/False       -- if we managed(or not) to insert the entry
            "comments":                 -- if we failed
        }
    """
    print("received ADD-ENTRY request")
    if request.is_json:
        data =request.json
        if (len(data) == 2) and ('userID' in data) and ('itemID' in data):
            result = dh.insert_new_entry(data['userID'], data['itemID'])
            return jsonify(result)
        else:
             print("wrong JSON")
             return Response(response="Wrong JSON format", status=400)
    else:
        print("not JSON")
        return Response(response="Expected JSON", status=400)


@app.route("/signup", methods=["POST"])
def signup():
    """
        Method called when the user signs up

        It has to be a POST HTTP request, containing a JSON of the format:
        {
            "username": <user_name>
            "password": <password>
            "first_name": <first_name>
            "last_name": <last_name>
            "email": <email>
        }
    :return: A JSON of the format:
        {
            "success": True/ False          -- if the siginin was successful
            "comments":                     -- any comments if the success field is False
        }
    """
    print("Received a SIGNUP request!")
    if request.is_json:
        data = request.json
        if (len(data) == 5) and ('username' in data) and ('password' in data) \
            and ('first_name' in data) and ('last_name' in data) and ('email' in data):

            result = dh.signup(data['username'], data['password'], data['first_name'],
                                data['last_name'], data['email'])

            return jsonify(result)
        else:
            print("wrong JSON")
            return Response(response="Wrong JSON format", status=400)

    else:
        print("not JSON")
        return Response(response="Expected JSON", status=400)

@app.route("/signin", methods=["POST"])
def signin():
    """
        Method called when the user tries to signin

        It expects a POST HTTP request containting a JSON of the format:
            {
                "username": <user_name>
                "password": <password>
            }

    :return: A JSON of the format:

            {
                "success": True/ False  -- if the singin was successful
                "id": <userID>          -- the ID corresponding to this user.
                                        It is used by the client app for further queries
            }
    """
    print("Received SIGNIN request!")
    if request.is_json:
        data = request.json
        if (len(data) == 2) and ('username' in data) and ('password' in data):
            result = dh.check_signin(data['username'], data['password'])
            return jsonify(result)
        else:
            print("Wrong JSON format")
            return Response(response="Expected JSON", status=400)
    else:
        print("not JSON")
        return Response(response="Expected JSON", status=400)


@app.route("/", methods=["GET"])
def home() :
    return "Welcome to the SORTbot server!"

if __name__ == "__main__":
    app.run(debug=True)
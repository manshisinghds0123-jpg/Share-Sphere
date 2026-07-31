from flask import Flask, request, jsonify

app = Flask(__name__)

USERS_FILE = "users.txt"
ITEMS_FILE = "items.txt"
REQUEST_FILE = "request.txt"


@app.route("/")
def home():
    return jsonify({
        "message": "ShareSphere API Running"
    })


# Register User
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data["name"]
    email = data["email"]
    phone = data["phone"]
    college = data["college"]
    password = data["password"]

    with open(USERS_FILE, "a") as file:
        file.write(
            f"{name},{email},{phone},{college},{password}\n"
        )

    return jsonify({
        "message": "Registration successful"
    })


# Login User
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]

    with open(USERS_FILE, "r") as file:
        users = file.readlines()

    for user in users:
        details = user.strip().split(",")

        if details[1] == email and details[4] == password:
            return jsonify({
                "message": "Login successful",
                "name": details[0]
            })

    return jsonify({
        "message": "Invalid credentials"
    }), 401


# Donate Item
@app.route("/donate", methods=["POST"])
def donate():

    data = request.json

    item = data["item"]
    category = data["category"]
    condition = data["condition"]
    description = data["description"]
    owner = data["owner"]

    with open(ITEMS_FILE, "a") as file:
        file.write(
            f"{owner},{item},{category},{condition},{description}\n"
        )

    return jsonify({
        "message": "Item donated successfully"
    })


# View Items
@app.route("/items", methods=["GET"])
def items():

    all_items = []

    with open(ITEMS_FILE, "r") as file:
        for line in file:
            data = line.strip().split(",")

            all_items.append({
                "owner": data[0],
                "item": data[1],
                "category": data[2],
                "condition": data[3],
                "description": data[4]
            })

    return jsonify(all_items)


# Request Item
@app.route("/request-item", methods=["POST"])
def request_item():

    data = request.json

    user = data["user"]
    item = data["item"]

    with open(REQUEST_FILE, "a") as file:
        file.write(
            f"{user},{item},Pending\n"
        )

    return jsonify({
        "message": "Request sent successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)
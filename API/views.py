from flask import request, jsonify, make_response, render_template
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
from functools import wraps
from API.app import app, db
from DB.models import Users, Person
from sqlalchemy import Date, cast


# Create token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
            current_user = Users.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


##############################################################################
# Person Views
##############################################################################

# Return all people in database
@app.route("/person", methods=["GET"])
@token_required
def get_all_people(current_user):
    people = Person.query.all()
    output = list()

    for person in people:
        person_data = dict()
        person_data["db_id"] = person.db_id
        person_data["id"] = person.id
        person_data["name"] = person.name
        person_data["date"] = person.date
        person_data["manner_of_death"] = person.manner_of_death
        person_data["armed"] = person.armed
        person_data["age"] = person.age
        person_data["gender"] = person.gender
        person_data["race"] = person.race
        person_data["city"] = person.city
        person_data["state"] = person.state
        person_data["signs_of_mental_illness"] = person.signs_of_mental_illness
        person_data["threat_level"] = person.threat_level
        person_data["flee"] = person.flee
        person_data["body_camera"] = person.body_camera
        person_data["longitude"] = person.longitude
        person_data["latitude"] = person.latitude
        person_data["is_geocoding_exact"] = person.is_geocoding_exact
        output.append(person_data)
    return jsonify({"people": output})  #


# Return person based on public ID
@app.route("/person/<id>", methods=["GET"])
@token_required
def get_person(current_user, id):
    person = Person.query.filter_by(id=id).first()

    if not person:
        return jsonify({"message": "No person found with this id"})

    person_data = dict()
    person_data["db_id"] = person.db_id
    person_data["id"] = person.id
    person_data["name"] = person.name
    person_data["date"] = person.date
    person_data["manner_of_death"] = person.manner_of_death
    person_data["armed"] = person.armed
    person_data["age"] = person.age
    person_data["gender"] = person.gender
    person_data["race"] = person.race
    person_data["city"] = person.city
    person_data["state"] = person.state
    person_data["signs_of_mental_illness"] = person.signs_of_mental_illness
    person_data["threat_level"] = person.threat_level
    person_data["flee"] = person.flee
    person_data["body_camera"] = person.body_camera
    person_data["longitude"] = person.longitude
    person_data["latitude"] = person.latitude
    person_data["is_geocoding_exact"] = person.is_geocoding_exact

    return jsonify({"users": person_data})


# parameterized query
@app.route("/person/params", methods=["GET"])
@token_required
def get_person_parameterized(current_user):
    age = request.args.get("age")
    armed = request.args.get("armed")
    body_camera = request.args.get("body_camera")
    city = request.args.get("city")
    leading_date = request.args.get("ldate")
    trailing_date = request.args.get("tdate")
    flee = request.args.get("flee")
    gender = request.args.get("gender")
    is_geocoding_exact = request.args.get("is_geocoding_exact")
    manner_of_death = request.args.get("manner_of_death")
    name = request.args.get("name")
    race = request.args.get("race")
    signs_of_mental_illness = request.args.get("signs_of_mental_illness")
    state = request.args.get("state")
    threat_level = request.args.get("threat_level")
    people = Person.query.filter()
    if age:
        people = people.filter(Person.age == age)
    if armed:
        if armed == 'unarmed':
            people = people.filter(Person.armed == armed)
        elif armed == 'armed':
            people = people.filter(Person.armed != 'unarmed')
    if body_camera:
        people = people.filter(Person.body_camera == bool(body_camera))
    if city:
        people = people.filter(Person.city == city)
    if leading_date and trailing_date:
        people = people.filter(cast(Person.date, Date).between(datetime.date(int(leading_date), 1, 1), datetime.date(int(trailing_date), 12, 31)))
        print(Person.date)
    if flee:
        if flee == 'Not fleeing':
            people = people.filter(Person.flee == flee)
        else:
            people = people.filter(Person.flee != "Not fleeing")
    if gender:
        people = people.filter(Person.gender == gender)
    if is_geocoding_exact:
        people = people.filter(Person.is_geocoding_exact == bool(is_geocoding_exact))
    if manner_of_death:
        people = people.filter(Person.manner_of_death == manner_of_death)
    if name:
        people = people.filter(Person.name == name)
    if race:
        people = people.filter(Person.race == race)
    if signs_of_mental_illness:
        people = people.filter(
            Person.signs_of_mental_illness == bool(signs_of_mental_illness)
        )
    if state:
        people = people.filter(Person.state == state)
    if threat_level:
        people = people.filter(Person.threat_level == threat_level)

    if not people:
        return jsonify({"message": "No person found with this id"})
    output = list()

    for person in people:
        person_data = dict()
        person_data["db_id"] = person.db_id
        person_data["id"] = person.id
        person_data["name"] = person.name
        person_data["date"] = person.date
        person_data["manner_of_death"] = person.manner_of_death
        person_data["armed"] = person.armed
        person_data["age"] = person.age
        person_data["gender"] = person.gender
        person_data["race"] = person.race
        person_data["city"] = person.city
        person_data["state"] = person.state
        person_data["signs_of_mental_illness"] = person.signs_of_mental_illness
        person_data["threat_level"] = person.threat_level
        person_data["flee"] = person.flee
        person_data["body_camera"] = person.body_camera
        person_data["longitude"] = person.longitude
        person_data["latitude"] = person.latitude
        person_data["is_geocoding_exact"] = person.is_geocoding_exact

        output.append(person_data)
    return jsonify({"people": output})


@app.route("/person/<id>", methods=["PUT"])
@token_required
def update_person(current_user, id):
    person = Person.query.filter_by(id=id).first()
    if not person:
        return jsonify({"message": "person not found"})
    data = request.get_json()
    updated_person = Person(
        id=str(data["id"]),
        name=data["name"],
        date=data["date"],
        manner_of_death=data["manner_of_death"],
        armed=data["armed"],
        age=data["age"],
        gender=data["gender"],
        race=data["race"],
        city=data["city"],
        state=data["state"],
        signs_of_mental_illness=data["signs_of_mental_illness"],
        threat_level=data["threat_level"],
        flee=data["flee"],
        body_camera=data["body_camera"],
        longitude=data["longitude"],
        latitude=data["latitude"],
        is_geocoding_exact=data["is_geocoding_exact"],
    )
    person.name = updated_person.name
    person.date = updated_person.date
    person.manner_of_death = updated_person.manner_of_death
    person.armed = updated_person.armed
    person.age = updated_person.age
    person.gender = updated_person.gender
    person.race = updated_person.race
    person.city = updated_person.city
    person.state = updated_person.state
    person.signs_of_mental_illness = updated_person.signs_of_mental_illness
    person.threat_level = updated_person.threat_level
    person.flee = updated_person.flee
    person.body_camera = updated_person.body_camera
    person.longitude = updated_person.longitude
    person.latitude = updated_person.latitude
    person.is_geocoding_exact = updated_person.is_geocoding_exact
    db.session.commit()
    return jsonify({"message": f"Person record {id} updated."})


# Add person to database
# Admin == True REQUIRED
@app.route("/person", methods=["POST"])
@token_required
def add_person(current_user):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function."})

    data = request.get_json()
    new_person = Person(
        id=str(data["id"]),
        name=data["name"],
        date=data["date"],
        manner_of_death=data["manner_of_death"],
        armed=data["armed"],
        age=data["age"],
        gender=data["gender"],
        race=data["race"],
        city=data["city"],
        state=data["state"],
        signs_of_mental_illness=data["signs_of_mental_illness"],
        threat_level=data["threat_level"],
        flee=data["flee"],
        body_camera=data["body_camera"],
        longitude=data["longitude"],
        latitude=data["latitude"],
        is_geocoding_exact=data["is_geocoding_exact"],
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify({"message": "New person added to database."})


@app.route("/person/<id>", methods=["DELETE"])
@token_required
def delete_person(current_user, id):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function."})

    person = Person.query.filter_by(id=id).first()
    if not person:
        return jsonify({"message": "No user found"})
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "No person found with this id"})


#############################################################################################
# User Views
#############################################################################################


@app.route("/user", methods=["GET"])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function."})

    users = Users.query.all()
    output = list()

    for user in users:
        user_data = {}
        user_data["public_id"] = user.public_id
        user_data["name"] = user.name
        user_data["password"] = user.password
        user_data["admin"] = user.admin
        output.append(user_data)
    return jsonify({"users": output})


@app.route("/user/<public_id>", methods=["GET"])
@token_required
def get_one_user(current_user, public_id):
    user = Users.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "No user found"})
    user_data = dict()
    user_data["public_id"] = user.public_id
    user_data["name"] = user.name
    user_data["password"] = user.password
    user_data["admin"] = user.admin

    return jsonify({"user": user_data})


@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data["password"], method="sha256")

    new_user = Users(
        public_id=str(uuid.uuid4()),
        name=data["name"],
        password=hashed_password,
        admin=False,
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "New user created!!"})


@app.route("/user/<public_id>", methods=["PUT"])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function."})

    user = Users.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "No user found"})

    user.admin = True
    db.session.commit()

    return jsonify({"message": "User has been promoted"})


@app.route("/user/<public_id>", methods=["DELETE"])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function."})

    user = Users.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": "No user found"})
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})


@app.route("/login")
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )

    user = Users.query.filter_by(name=auth.username).first()

    if not user:
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )
        return jsonify({"token": token})

    return make_response(
        "Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )


#################################################################################################################################################
# Map STUFF
################################################################################################################################################
@app.route("/map")
def map():
    return render_template("map.html")

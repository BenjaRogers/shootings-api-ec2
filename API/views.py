from flask import request, jsonify, make_response, render_template
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
from functools import wraps
from API.app import app, db
from DB.models import Users, Person, Agency
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
        person_data["body_camera"] = person.body_camera
        person_data["city"] = person.city
        person_data["county"] = person.county
        person_data["state"] = person.state
        person_data["longitude"] = person.longitude
        person_data["latitude"] = person.latitude
        person_data["location_precision"] = person.location_precision
        person_data["age"] = person.age
        person_data["gender"] = person.gender
        person_data["race"] = person.race
        person_data["race_source"] = person.race_source
        person_data["was_mental_illness_related"] = person.was_mental_illness_related
        person_data["threat_type"] = person.threat_type
        person_data["armed_with"] = person.armed_with
        person_data["flee_status"] = person.flee_status
        person_data["agency_ids"] = person.agency_ids

        output.append(person_data)
    return jsonify({"people": output})


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
    person_data["body_camera"] = person.body_camera
    person_data["city"] = person.city
    person_data["county"] = person.county
    person_data["state"] = person.state
    person_data["longitude"] = person.longitude
    person_data["latitude"] = person.latitude
    person_data["location_precision"] = person.location_precision
    person_data["age"] = person.age
    person_data["gender"] = person.gender
    person_data["race"] = person.race
    person_data["race_source"] = person.race_source
    person_data["was_mental_illness_related"] = person.was_mental_illness_related
    person_data["threat_type"] = person.threat_type
    person_data["armed_with"] = person.armed_with
    person_data["flee_status"] = person.flee_status
    person_data["agency_ids"] = person.agency_ids

    return jsonify({"people": person_data})


# parameterized query
@app.route("/person/params", methods=["GET"])
@token_required
def get_person_parameterized(current_user):

    age = request.args.get("age")
    armed_with = request.args.get("armed_with")
    body_camera = request.args.get("body_camera")
    city = request.args.get("city")
    leading_date = request.args.get("ldate")
    trailing_date = request.args.get("tdate")
    flee_status = request.args.get("flee_status")
    gender = request.args.get("gender")
    location_precision = request.args.get("location_precision")
    name = request.args.get("name")
    race = request.args.get("race")
    was_mental_illness_related = request.args.get("was_mental_illness_related")
    state = request.args.get("state")
    threat_type = request.args.get("threat_type")

    people = Person.query.filter()

    if age:
        people = people.filter(Person.age == age)
    if armed_with == "unarmed":
        people = people.filter(Person.armed == armed_with)
    if armed_with == "armed":
        people = people.filter(Person.armed != "unarmed")
    if body_camera:
        people = people.filter(Person.body_camera == bool(body_camera))
    if city:
        people = people.filter(Person.city == city)
    if leading_date and trailing_date:
        people = people.filter(cast(Person.date, Date).between(datetime.date(int(leading_date), 1, 1), datetime.date(int(trailing_date), 12, 31)))
    if flee_status:
        if flee_status == 'Not fleeing':
            people = people.filter(Person.flee == flee_status)
    if gender:
        people = people.filter(Person.gender == gender)
    if location_precision:
        people = people.filter(Person.is_geocoding_exact == bool(location_precision))
    if name:
        people = people.filter(Person.name == name)
    if race:
        people = people.filter(Person.race == race)
    if was_mental_illness_related:
        people = people.filter(
            Person.signs_of_mental_illness == bool(was_mental_illness_related)
        )
    if state:
        people = people.filter(Person.state == state)
    if threat_type:
        people = people.filter(Person.threat_level == threat_type)

    if not people:
        return jsonify({"message": "No person found with this id"})
    output = list()

    for person in people:
        person_data = dict()
        person_data["db_id"] = person.db_id
        person_data["id"] = person.id
        person_data["name"] = person.name
        person_data["date"] = person.date
        person_data["body_camera"] = person.body_camera
        person_data["city"] = person.city
        person_data["county"] = person.county
        person_data["state"] = person.state
        person_data["longitude"] = person.longitude
        person_data["latitude"] = person.latitude
        person_data["location_precision"] = person.location_precision
        person_data["age"] = person.age
        person_data["gender"] = person.gender
        person_data["race"] = person.race
        person_data["race_source"] = person.race_source
        person_data["was_mental_illness_related"] = person.was_mental_illness_related
        person_data["threat_type"] = person.threat_type
        person_data["armed_with"] = person.armed_with
        person_data["flee_status"] = person.flee_status
        person_data["agency_ids"] = person.agency_ids

        output.append(person_data)
    return jsonify({"people": output})


@app.route("/person/<id>", methods=["PUT"])
@token_required
def update_person(current_user, id):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function."})
    person = Person.query.filter_by(id=id).first()
    if not person:
        return jsonify({"message": "person not found"})
    data = request.get_json()
    updated_person = Person(
        id=str(data["id"]),
        name=data["name"],
        date=data["date"],
        body_camera=data["body_camera"],
        city=data["city"],
        county=data["county"],
        state=data["state"],
        longitude=data["longitude"],
        latitude=data["latitude"],
        location_precision=data["location_precision"],
        age=data["age"],
        gender=data["gender"],
        race=data["race"],
        race_source=data["race_source"],
        was_mental_illness_related=data["was_mental_illness_related"],
        threat_type=data["threat_type"],
        armed_with=data["armed_with"],
        flee_status=data["flee_status"],
        agency_ids=data["agency_ids"],
    )
    person.name = updated_person.name
    person.date = updated_person.date
    person.body_camera = updated_person.body_camera
    person.city = updated_person.city
    person.county = updated_person.county
    person.state = updated_person.state
    person.longitude = updated_person.longitude
    person.latitude = updated_person.latitude
    person.location_precision = updated_person.location_precision
    person.age = updated_person.age
    person.gender = updated_person.gender
    person.race = updated_person.race
    person.race_source = updated_person.race_source
    person.was_mental_illness_related = updated_person.was_mental_illness_related
    person.threat_type = updated_person.threat_type
    person.armed_with = updated_person.armed_with
    person.flee_status = updated_person.flee_status
    person.agency_ids = updated_person.agency_ids

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
        body_camera=data["body_camera"],
        city=data["city"],
        county=data["county"],
        state=data["state"],
        longitude=data["longitude"],
        latitude=data["latitude"],
        location_precision=data["location_precision"],
        age=data["age"],
        gender=data["gender"],
        race=data["race"],
        race_source=data["race_source"],
        was_mental_illness_related=data["was_mental_illness_related"],
        threat_type=data["threat_type"],
        armed_with=data["armed_with"],
        flee_status=data["flee_status"],
        agency_ids=data["agency_ids"],
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
        return jsonify({"message": "No person found"})
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "Person removed"})


#############################################################################################
# Agency Views
#############################################################################################
# Return all agencies in database
@app.route("/agency", methods=["GET"])
@token_required
def get_all_agencies(current_user):
    agencies = Agency.query.all()
    output = list()

    for agency in agencies:
        agency_data = dict()

        agency_data["db_id"] = agency.db_id
        agency_data["id"] = agency.id
        agency_data["name"] = agency.name
        agency_data["type"] = agency.type
        agency_data["state"] = agency.state
        agency_data["oricodes"] = agency.oricodes
        agency_data["total_shootings"] = agency.total_shootings

        output.append(agency_data)
    return jsonify({"agencies": output})


# Return agency based on public ID
@app.route("/agency/<id>", methods=["GET"])
@token_required
def get_agency(current_user, id):
    agency = Agency.query.filter_by(id=id).first()

    if not agency:
        return jsonify({"message": "No agency found with this id"})

    agency_data = dict()

    agency_data["db_id"] = agency.db_id
    agency_data["id"] = agency.id
    agency_data["name"] = agency.name
    agency_data["type"] = agency.type
    agency_data["state"] = agency.state
    agency_data["oricodes"] = agency.oricodes
    agency_data["total_shootings"] = agency.total_shootings

    return jsonify({"agencies": agency_data})


# parameterized query
@app.route("/agency/params", methods=["GET"])
@token_required
def get_agency_parameterized(current_user):
    id_list = request.args.getlist("id")

    agencies = Agency.query.filter()

    if id_list:
        agencies = agencies.filter(Agency.id.in_(id_list))

    output = list()

    for agency in agencies:
        agency_data = dict()

        agency_data["db_id"] = agency.db_id
        agency_data["id"] = agency.id
        agency_data["name"] = agency.name
        agency_data["type"] = agency.type
        agency_data["state"] = agency.state
        agency_data["oricodes"] = agency.oricodes
        agency_data["total_shootings"] = agency.total_shootings

        output.append(agency_data)

    return jsonify({"agencies": output})


@app.route("/agency/<id>", methods=["PUT"])
@token_required
def update_agency(current_user, id):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function."})

    agency = Agency.query.filter_by(id=id).first()
    if not agency:
        return jsonify({"message": "agency not found"})
    data = request.get_json()
    updated_agency = Agency(
        id=str(data["id"]),
        name=data["name"],
        type=data["type"],
        state=data["state"],
        oricodes=data["oricodes"],
        total_shootings=data["total_shootings"]
    )
    agency.name = updated_agency.name
    agency.type = updated_agency.type
    agency.state = updated_agency.state
    agency.oricodes = updated_agency.oricodes
    agency.total_shootings = updated_agency.total_shootings

    db.session.commit()
    return jsonify({"message": f"Agency record {id} updated."})


# Add person to database
# Admin == True REQUIRED
@app.route("/agency", methods=["POST"])
@token_required
def add_agency(current_user):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function."})

    data = request.get_json()
    new_agency = Agency(
        id=str(data["id"]),
        name=data["name"],
        type=data["type"],
        state=data["state"],
        oricodes=data["oricodes"],
        total_shootings=data["total_shootings"]
    )

    db.session.add(new_agency)
    db.session.commit()

    return jsonify({"message": "New agency added to database."})


@app.route("/agency/<id>", methods=["DELETE"])
@token_required
def delete_agency(current_user, id):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function."})

    agency = Agency.query.filter_by(id=id).first()
    if not agency:
        return jsonify({"message": "No agency found"})
    db.session.delete(agency)
    db.session.commit()
    return jsonify({"message": "Agency removed"})


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
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function."})

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

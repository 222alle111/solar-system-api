from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from ..db import db
from .routes_utilities import validate_model

# created blueprint
planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    try:
        new_planet = Planet.from_dict(request_body)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_planet)
    db.session.commit()

    response = new_planet.to_dict()
    return response, 201

@planets_bp.get("")
def get_all_planets():

    query = db.select(Planet)

    name_param = request.args.get("name")
    if name_param:
        query = db.select(Planet).where(Planet.name == name_param)

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    size_param = request.args.get("size_dia_km")
    if size_param:
        query = query.where(Planet.size_dia_km.ilike(f"%{size_param}%"))
    

    query = query.order_by(Planet.id)
    planets = db.session.scalars(query)

    planets_response = [planet.to_dict() for planet in planets]
    return planets_response

    

@planets_bp.get("/<planet_id>")
def get_single_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    
    return planet.to_dict()

@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.size_dia_km = request_body["size_dia_km"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    db.session.delete(planet)
    db.session.commit()
    return Response(status=204, mimetype="application/json")


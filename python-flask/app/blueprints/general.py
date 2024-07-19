import sqlite3
import sqlalchemy
from flask import Blueprint
from flask import jsonify, request
from app.extensions.db import db
from app.models import Location, Elevation
from wyl.location.elevation import query_elevation
from wyl.location.query import query_location
from wyl.location.boundingbox import get_bb_points


bp_general = Blueprint('general', __name__)


def is_unique_elevation_entry(lat, lon):
    count = Elevation.query.filter_by(lat=lat, lon=lon).count()
    return count == 0


@bp_general.get('/')
async def general_index():
    query_param = request.args.get('q')
    if query_param is not None:
        if "|" in query_param:
            splitted_query_params = query_param.split("|")
            for query_param_s in splitted_query_params:
                current_location: dict = query_location(query_param_s)

                for p in get_bb_points(current_location.get('boundingbox').split(',')):
                    lat_, lon_ = p
                    elevation_results_ = query_elevation(lat_, lon_)
                    if isinstance(elevation_results_, float):
                        lat_lon_k = f"{lat_},{lon_}"
                        if is_unique_elevation_entry(lat_, lon_):
                            db_elevation_ = Elevation(lat=lat_, lon=lon_, elevation=elevation_results_)
                            db.session.add(db_elevation_)
                            db.session.commit()
                        else:
                            print(f"skipping: {lat_lon_k}")
                lat = current_location.get('lat')
                lon = current_location.get('lon')
                elevation_results = query_elevation(lat, lon)

                loc_ = Location(**current_location)
                if isinstance(elevation_results, float):
                    db_elevation = Elevation(lat=lat, lon=lon, elevation=elevation_results)

                    db.session.add(db_elevation)
                    loc_.elevation = elevation_results

                db.session.add(loc_)
                try:
                    db.session.commit()
                except sqlite3.IntegrityError as ie:
                    print("ie")
                    print(ie)
                except sqlalchemy.exc.IntegrityError as sie:
                    print("sie")
                    print(sie)
                    db.session.rollback()

        else:
            current_location: dict = query_location(query_param)

            for p in get_bb_points(current_location.get('boundingbox').split(',')):
                lat_, lon_ = p
                elevation_results_ = query_elevation(lat_, lon_)
                if isinstance(elevation_results_, float):
                    db_elevation_ = Elevation(lat=lat_, lon=lon_, elevation=elevation_results_)
                    db.session.add(db_elevation_)
            lat = current_location.get('lat')
            lon = current_location.get('lon')
            elevation_results = query_elevation(lat, lon)

            loc_ = Location(**current_location)
            if isinstance(elevation_results, float):
                db_elevation = Elevation(lat=lat, lon=lon, elevation=elevation_results)
                db.session.add(db_elevation)
                loc_.elevation = elevation_results

            db.session.add(loc_)
            try:
                db.session.commit()
            except sqlite3.IntegrityError as ie:
                print("ie")
                print(ie)
            except sqlalchemy.exc.IntegrityError as sie:
                print("sie")
                print(sie)
                db.session.rollback()

    else:
        print("no q parameter")
        print(db.session.query(Location).all())
        print(db.session.query(Elevation).all())

    entries = db.session.query(Location).all()

    return jsonify(json_list=[i.serialize for i in entries])

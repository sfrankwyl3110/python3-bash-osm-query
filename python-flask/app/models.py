from sqlalchemy import func
from app.extensions.db import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return f"{value.strftime("%Y-%m-%d")} {value.strftime("%H:%M:%S")}"


class Elevation(db.Model):
    __tablename__ = "elevations"
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    elevation = db.Column(db.Float)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())


class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(255), unique=True)

    place_id = db.Column(db.Integer, unique=True)

    osm_id = db.Column(db.Integer)
    osm_type = db.Column(db.String(255), nullable=False)

    boundingbox = db.Column(db.String(255))

    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    elevation = db.Column(db.Float)

    display_name = db.Column(db.String(255))

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if "elevation" not in kwargs.keys():
            self.elevation = 0.0

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            '_id': self.id,
            'query': self.query,
            'lat': self.lat,
            'lon': self.lon,
            'elevation': self.elevation,
            'display_name': self.display_name,
            'boundingbox': self.boundingbox,
            'place_id': self.place_id,
            'osm_id': self.osm_id,
            'osm_type': self.osm_type,
            'created_at': dump_datetime(self.created_at),
        }

    def __repr__(self):
        return f'<Location {self.query}>'

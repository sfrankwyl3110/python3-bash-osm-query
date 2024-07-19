from app import create_app
from app.blueprints.general import bp_general
from app.extensions.db import db
from app.models import Location, Elevation
from dotenv import load_dotenv

load_dotenv(".env")

app = create_app()
app.register_blueprint(bp_general)

with app.app_context():
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=5005, debug=True)

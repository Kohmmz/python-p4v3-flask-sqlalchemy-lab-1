# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response,jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquakes(id):
    earthquakes = Earthquake.query.get(id)
    if earthquakes:
        return make_response(jsonify(earthquakes.to_dict()),200)
    return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    return jsonify({
        "count": len(earthquakes),
        "quakes": [quake.to_dict() for quake in earthquakes]
    })


if __name__ == '__main__':
    app.run(port=5555, debug=True)

#!/usr/bin/python3
"""
The Flask-App integrating with Air-BnB HTML Temp.
"""
from flask import Flask, render_template, url_for
from models import storage
from uuid import uuid4

app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closing after every requist over going SQL-Alchemy Sesion.
    """
    storage.close()


@app.route('/0-hbnb')
def hbnb_filters(the_id=None):
    """
    Handeling the request of templete with state, city and amenty.
    """
    cache_id = uuid4()
    state_objs = storage.all('State').values()
    states = dict([state.name, state] for state in state_objs)
    amens = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
                 for user in storage.all('User').values())
    return render_template('0-hbnb.html',
                           states=states,
                           amens=amens,
                           places=places,
                           users=users,
                           cache_id=cache_id)

if __name__ == "__main__":
    app.run(host=host, port=port)

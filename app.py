from flask import render_template, Flask, session
from blueprints.query.blueprint import blueprint_query
from blueprints.auth.auth import blueprint_auth
from blueprints.report.route import blueprint_report
from blueprints.basket.route import blueprint_order
import model.app_model as model
import os
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20).hex()
for file in os.listdir(os.path.join(os.path.dirname(__file__), 'json')):
    with open(f'./json/{file}') as f:
        app.config[file] = json.load(f)

app.config['db_config'] = app.config['undefined_db_config.json']
app.config['auth_db_config'] = app.config['db_config']

app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_order, url_prefix='/order')


@app.route('/')
def home_page():
    ct = model.home(app.config['undefined_db_config.json'])
    return render_template('home_page.html', context=ct)


@app.route('/film/<name>')
def film_info(name):
    html, ct = model.film(app.config['undefined_db_config.json'], name)
    return render_template(html, context=ct)


@app.route('/main_menu')
def main_menu():
    ui = session.get('user_id', None)
    access = app.config['access.json'].get(session.get('user_group', None), [])
    return render_template('main_menu.html', ui=ui, access=access)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)

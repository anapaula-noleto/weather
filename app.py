import requests
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy(app)


# serve para criar a tabela city no banco de dados
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=pt_br&appid=3540f061174193d30c97f2ac495cffed"
    r = requests.get(url).json()
    return r


@app.route("/")
def index_get():
    cities = City.query.all()

    weather_data = []

    for city in cities:
        r = get_weather_data(city.name)
        # dicionário que vai armazenar as informações que vou usar
        weather = {
            'city': city.name,
            'country': r['sys']['country'],
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'].capitalize(),
            'icon': r['weather'][0]['icon'],
            'wind_speed': r['wind']['speed'],
            'max_temperature': r['main']['temp_max'],
            'humidity': r['main']['humidity']
        }
        weather_data.append(weather)
    # print(weather_data)
    return render_template("index.html", weather_data=weather_data)


@app.route("/", methods=['POST'])
def index_post():
    extras = request.form.getlist('mycheckbox')
    print(extras)
    error_msg = ''
    new_city = request.form.get("city").strip()

    if new_city:
        # Query the table to check if the city is already in there.
        existing_city = City.query.filter_by(name=new_city).first()
        if not existing_city:
            new_city_data = get_weather_data(new_city)
            print("cod:",new_city_data['cod'])
            if new_city_data['cod'] == 200:
                # add the new city to the database
                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                error_msg = f'Não foi localizada a cidade com o nome {new_city}'
        else:
            error_msg = 'A cidade já foi salva'
    else:
        error_msg = 'Digite uma cidade válida'
    if error_msg:
        flash(error_msg, 'error')
    else:
        flash(f'A cidade {new_city} foi adicionada com sucesso')

    return redirect(url_for('index_get'))


@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()
    flash(f'A cidade {city.name} foi deletada com sucesso')
    return redirect(url_for('index_get'))


if __name__ == "__main__":
    app.run(debug=True)

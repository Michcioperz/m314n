import os
from importlib import import_module

from flask import Flask, redirect, render_template, request, url_for
from flask.ext.babel import Babel
from redis import Redis

app = Flask(__name__)
app.config.from_json(os.getenv("M314_CONFIG", "m314.json"))
babel = Babel(app)

assert 'REDIS_DB' in app.config
redis = Redis(db=app.config.get('REDIS_DB', 314))

assert 'WIDGETS' in app.config
widgets = []
for widget_pkg in app.config['WIDGETS']:
    pkg = import_module(widget_pkg)
    widgets.append(pkg(appcfg=app.config, redis=redis))


@babel.localeselector
def get_locale():
    if "lang" in request.view_args:
        return request.view_args.get("lang", "en")
    return request.accept_languages.best_match(['en', 'pl', 'es'])


@app.route('/')
def homeguess():
    return redirect(url_for("homepage", lang=get_locale()))


@app.route('/<lang>/')
def homepage(lang: str):
    return render_template("index.html", lang=lang, widgets=widgets)


if __name__ == '__main__':
    app.run()

import json

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
from flask import Blueprint, render_template
from flask_nav.elements import Navbar, View

from .forms import NormalPidForm
from .nav import nav

frontend = Blueprint('frontend', __name__)

nav.register_element('frontend_top', Navbar(
    View('ISS Project', '.index'),
    View('Classic PID', '.classic_pid'),
    View('Fancy PID', '.fancy_pid'),
))


@frontend.route('/')
def index():
    bar = create_plot()
    return render_template('index.html', plot=bar)


@frontend.route('/classic_pid/', methods=('GET', 'POST'))
def classic_pid():
    form = NormalPidForm()

    if form.validate_on_submit():
        form.hole_r.render_kw = {'disabled': 'disabled'}
        bar = create_plot()
        return render_template('normalPid.html', form=form, plot=bar)

    return render_template('normalPid.html', form=form)


def create_plot():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    y2 = np.ones(N)
    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
    df2 = pd.DataFrame({'x': x, 'y': y2})  # creating a sample dataframe
    data = [
        go.Scatter(
            x=df['x'],
            y=df['y'],
            mode='lines',
            name='Otrzymana wartość'
        ),
        go.Scatter(
            x=df2['x'],
            y=df2['y'],
            mode='lines',
            name='Wartość zadana'
        )

    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@frontend.route('/fancy_pid/', methods=('GET', 'POST'))
def fancy_pid():
    form = NormalPidForm()

    if form.validate_on_submit():
        bar = create_plot()
        return render_template('normalPid.html', form=form, plot=bar)

    return render_template('normalPid.html', form=form)

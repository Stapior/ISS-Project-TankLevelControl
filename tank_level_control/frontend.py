import json
import math

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
        bar = simulate()
        return render_template('normalPid.html', form=form, plot=bar)

    return render_template('normalPid.html', form=form)


def simulate():
    time = 200.0
    step = 0.01
    startLevel = 70.0
    outputFactor = 20.0
    givenLevel = 50.0
    surfaceArea = 20.0

    n = math.ceil(time / step)
    result = [startLevel]
    inputs = [0]
    steps = [0]
    suma = 0
    for i in range(0, n):
        currentH = result[len(result) - 1]
        suma += givenLevel - currentH
        inputVolume = getInputIntensity(givenLevel, currentH, suma) * step
        inputs.append(inputVolume / step)
        outputVolume = outputFactor * math.sqrt(currentH) * step
        result.append(currentH + ((inputVolume - outputVolume) / surfaceArea))

        steps.append(steps[len(steps) - 1] + step)

    df = pd.DataFrame({'x': steps, 'y': result})  # creating a sample dataframe
    di = pd.DataFrame({'x': steps, 'y': inputs})  # creating a sample dataframe
    data = [
        go.Scatter(
            x=df['x'],
            y=df['y'],
            mode='lines',
            name='Otrzymana wartość'
        ),
        go.Scatter(
            x=di['x'],
            y=di['y'],
            mode='lines',
            name='Otrzymana wartość'
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def getInputIntensity(target, current, suma):
    if current < target:
        u = target - current
        return 10 * u + suma
    else:
        return 0


@frontend.route('/fancy_pid/', methods=('GET', 'POST'))
def fancy_pid():
    form = NormalPidForm()

    if form.validate_on_submit():
        bar = simulate()
        return render_template('normalPid.html', form=form, plot=bar)

    return render_template('normalPid.html', form=form)

import json
import math

import pandas as pd
import plotly
import plotly.graph_objs as go
from flask import Blueprint, render_template
from flask_nav.elements import Navbar, View

from .PID import PID
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
    return render_template('index.html')


@frontend.route('/classic_pid/', methods=('GET', 'POST'))
def classic_pid():
    form = NormalPidForm()

    if form.validate_on_submit():
        area = math.pow(form.tank_r.data, 2) * math.pi
        bar = simulate(form.time.data, form.step.data, form.start_level.data, form.given_level.data, area,
                       form.outputFactor.data, form.Kp.data, form.Ki.data, form.Kd.data)
        return render_template('normalPid.html', form=form, plot=bar)

    return render_template('normalPid.html', form=form)


def simulate(time: float, step: float, startLevel: float, givenLevel: float, surfaceArea: float, outputFactor: float,
             Kp: float, Ki: float, Kd: float):
    n = math.ceil(time / step)
    results = [startLevel]
    inputs = [0.0]
    steps = [0]

    pid = PID(Kp, Ki, Kd)
    pid.setPoint(givenLevel)

    for i in range(1, n):
        currentH = results[i - 1]
        inputIntensity = max(pid.update(currentH), 0.0)
        inputVolume = inputIntensity * step
        outputVolume = outputFactor * math.sqrt(currentH) * step
        heightChange = ((inputVolume - outputVolume) / surfaceArea)

       # inputs.append(inputIntensity)
        results.append(currentH + heightChange)
        steps.append(i * step)

    return getGraph(givenLevel, results, steps)


def getGraph(givenLevel, results, steps):
    df = pd.DataFrame({'x': steps, 'y': results})
    di = pd.DataFrame({'x': steps, 'y': givenLevel})
    data = [
        go.Scatter(
            x=df['x'],
            y=df['y'],
            mode='lines',
            name='Otrzymane wartości'
        ),
        go.Scatter(
            x=di['x'],
            y=di['y'],
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
        return render_template('normalPid.html', form=form)

    return render_template('normalPid.html', form=form)

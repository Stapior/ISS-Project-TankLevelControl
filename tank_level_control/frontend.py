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
        (bar, errorAbsSum) = simulate(form.time.data, form.step.data, form.start_level.data, form.given_level.data,
                                      area,
                                      form.outputFactor.data, form.Kp.data, form.Ki.data, form.Kd.data)
        return render_template('normalPid.html', form=form, plot=bar, errorAbsSum=errorAbsSum)

    return render_template('normalPid.html', form=form)


def simulate(time: float, step: float, startLevel: float, givenLevel: float, surfaceArea: float, outputFactor: float,
             Kp: float, Ki: float, Kd: float):
    n = math.ceil(time / step)
    results = [startLevel]
    inputs = [0.0]
    steps = [0]

    pid = PID(Kp, Ki, Kd)
    pid.setPoint(givenLevel)
    errorAbsSum = 0

    for i in range(1, n):
        currentH = results[i - 1]

        inputIntensity = max(pid.update(currentH, i * step), 0)
        errorAbsSum += abs(givenLevel - currentH) * step

        inputVolume = inputIntensity * step
        outputVolume = outputFactor * math.sqrt(currentH) * step
        heightChange = (inputVolume - outputVolume) / surfaceArea

        inputs.append(inputIntensity)
        results.append(max(currentH + heightChange, 0))
        steps.append(i * step)

    return getGraph(givenLevel, results, steps, inputs), errorAbsSum


def getGraph(givenLevel, results, steps, inputs):
    df_results = pd.DataFrame({'x': steps, 'y': results})
    df_point = pd.DataFrame({'x': steps, 'y': givenLevel})
    df_inputs = pd.DataFrame({'x': steps, 'y': inputs})
    data = [
        go.Scatter(
            x=df_results['x'],
            y=df_results['y'],
            mode='lines',
            name='Otrzymane wartości'
        ),
        go.Scatter(
            x=df_point['x'],
            y=df_point['y'],
            mode='lines',
            name='Wartość zadana'
        ),
        go.Scatter(
            x=df_inputs['x'],
            y=df_inputs['y'],
            mode='lines',
            name='Wartości sterowania',
            visible=False,
            showlegend=True
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

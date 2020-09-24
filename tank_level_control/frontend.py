import json
import math

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
from flask import Blueprint, render_template
from flask_nav.elements import Navbar, View

from .Fuzzy import Fuzzy
from .PID import PID
from .forms import NormalPidForm, QualityOptimizationPid, FuzzyController
from .nav import nav

frontend = Blueprint('frontend', __name__)

nav.register_element('frontend_top', Navbar(
    View('ISS Project', '.index'),
    View('Klasyczny PID', '.classic_pid'),
    View('PID-jakość sterowania', '.quality_pid'),
    View('Regulator PID Rozmyty', '.fuzzy_pid'),
))


@frontend.route('/')
def index():
    return render_template('index.html')


@frontend.route('/classic_pid/', methods=('GET', 'POST'))
def classic_pid():
    form = NormalPidForm()

    if form.validate_on_submit():
        (bar, errorAbsSum) = simulatePid(form.time.data, form.step.data, form.start_level.data, form.given_level.data,
                                         form.tank_area.data, form.outputFactor.data, form.Kp.data, form.Ki.data,
                                         form.Kd.data)
        return render_template('normalPid.html', form=form, plot=bar, errorAbsSum=errorAbsSum)

    return render_template('normalPid.html', form=form)


def simulatePid(time: float, step: float, startLevel: float, givenLevel: float, surfaceArea: float, outputFactor: float,
                Kp: float, Ki: float, Kd: float):
    n = math.ceil(time / step)
    results = [startLevel]
    inputs = [0.0]
    steps = [0]
    pid = PID(Kp, Ki, Kd)
    pid.setPoint(givenLevel)
    errorAbsSum = 0
    last_intensity = 0
    maxIntensity = outputFactor * math.sqrt(givenLevel) * 50
    maxChangeForSecond = 0.05 * maxIntensity
    print(maxIntensity)

    for i in range(1, n):
        currentH = results[i - 1]

        error = givenLevel - currentH
        errorAbsSum += abs(error) * step
        target_intensity = max(pid.update(currentH, i * step), 0)

        last_intensity = getInputIntensity(last_intensity, target_intensity, maxChangeForSecond, maxIntensity, step)
        inputVolume = last_intensity * step

        outputVolume = outputFactor * math.sqrt(currentH) * step
        heightChange = (inputVolume - outputVolume) / surfaceArea

        inputs.append(last_intensity)
        results.append(max(currentH + heightChange, 0))
        steps.append(i * step)

    return getGraph(givenLevel, results, steps, inputs), errorAbsSum


def getInputIntensity(last_intensity, target_intensity, maxChangeForSecond, max_intensity, step):
    change = target_intensity - last_intensity
    if maxChangeForSecond * step < abs(change):
        intensity = last_intensity + (np.sign(change) * (maxChangeForSecond * step))
    else:
        intensity = target_intensity

    return max(min(max_intensity, intensity),0)


@frontend.route('/quality_pid/', methods=('GET', 'POST'))
def quality_pid():
    form = QualityOptimizationPid()


    if form.validate_on_submit():

        (bar, errorAbsSum) = simulateQulityPid(form.time.data, form.step.data, form.start_level.data,
                                               form.given_level.data,
                                               form.tank_area.data, form.outputFactor.data, form.Kp.data, form.Ki.data,
                                               form.Kd.data, form.testField.data)
        return render_template('pidQualityMeasure.html', form=form, plot=bar, errorAbsSum=errorAbsSum)

    return render_template('pidQualityMeasure.html', form=form)


def simulateQulityPid(time: float, step: float, startLevel: float, givenLevel: float, surfaceArea: float,
                      outputFactor: float,
                      Kp: float, Ki: float, Kd: float, value: int):
    n = math.ceil(time / step)
    results = [startLevel]
    inputs = [0.0]
    steps = [0]
    pid = PID(Kp, Ki, Kd)
    pid.setPoint(givenLevel)
    errorAbsSum = 0
    inputIntensity = 0

    for i in range(1, n):
        currentH = results[i - 1]
        if value == '1':
            inputIntensity = max(pid.wskaznikJakosci(currentH, i * step, 1), 0)
        elif value == '2':
            inputIntensity = max(pid.wskaznikJakosci(currentH, i * step, 2), 0)
        elif value == '3':
            inputIntensity = max(pid.wskaznikJakosci(currentH, i * step, 3), 0)
        elif value == '4':
            inputIntensity = max(pid.wskaznikJakosci(currentH, i * step, 4), 0)
        elif value == '5':
            inputIntensity = max(pid.wskaznikJakosci(currentH, i * step, 5), 0)

        errorAbsSum += abs(givenLevel - currentH) * step

        inputVolume = inputIntensity * step
        outputVolume = outputFactor * math.sqrt(currentH) * step
        heightChange = (inputVolume - outputVolume) / surfaceArea

        inputs.append(inputIntensity)
        results.append(max(currentH + heightChange, 0))
        steps.append(i * step)

    return getGraph(givenLevel, results, steps, inputs), errorAbsSum


def simulateFuzzyPid(time: float, step: float, startLevel: float, givenLevel: float, surfaceArea: float,
                     outputFactor: float):
    n = math.ceil(time / step)
    results = [startLevel]
    inputs = [0.0]
    steps = [0]
    fuzzy = Fuzzy()
    errorAbsSum = 0
    last_intensity = 0
    maxIntensity = outputFactor * math.sqrt(givenLevel) * 3
    maxChangeForSecond =0.2 * maxIntensity
    print(maxIntensity)

    for i in range(1, n):
        currentH = results[i - 1]

        error = givenLevel - currentH
        errorAbsSum += abs(error) * step
        target_intensity = (fuzzy.update(error, step) / 100.) * maxIntensity

        last_intensity = getInputIntensity(last_intensity, target_intensity, maxChangeForSecond, maxIntensity, step)
        inputVolume = last_intensity * step

        outputVolume = outputFactor * math.sqrt(currentH) * step
        heightChange = (inputVolume - outputVolume) / surfaceArea

        inputs.append(last_intensity/maxIntensity*100)
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




@frontend.route('/fuzzy_pid/', methods=('GET', 'POST'))
def fuzzy_pid():
    form = FuzzyController()

    if form.validate_on_submit():
        (bar, errorAbsSum) = simulateFuzzyPid(form.time.data, form.step.data, form.start_level.data,
                                              form.given_level.data,
                                              form.tank_area.data, form.outputFactor.data)
        return render_template('fuzzyPid.html', form=form, plot=bar, errorAbsSum=errorAbsSum)

    return render_template('fuzzyPid.html', form=form)

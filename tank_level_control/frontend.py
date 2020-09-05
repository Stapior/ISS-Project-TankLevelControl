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
    time = 200.0  #{ czas symulacji
    step = 0.01  # czzas jednego kroku
    startLevel = 70.0
    outputFactor = 20.0 # współczynnik wypływu, czyli ile wody wylatuje w 1 jednostce czasu przy wysokosci wody = 1
                        # współczynnik ten zależny jest od lepkosci cieczy, powierzchni otworu oraz jakiegos wspolczynnika zaworu
    givenLevel = 50.0 # zadany poziom wody (do tego dązymy w czasie regulacji)
    surfaceArea = 20.0   # pole powierzchni spodu zbiornika
                         # } te wartośi mogą być konfigurowalne, np z tego formularza który sie wyswietla na stronie

    n = math.ceil(time / step) # liczba kroków w symulacji
    result = [startLevel] # lista zawierająca poziomy wody w poszczególnych krokach symualcji
    inputs = [0] # wartości sterowania w czasie symulacji, czyli objętośc cieczy jaka ma wpływac do zbiornika, to wtylicza algorytm steroania np PID
    steps = [0] # wartości czasu dla każdego kroku (tylko do wykresu potrzebne)
    suma = 0 # suma uchybów dla PID
    for i in range(0, n):
        currentH = result[len(result) - 1] # aktualna wysokosc cieczy (wyliczona z poprzedniego korku)
        suma += givenLevel - currentH
        inputVolume = getInputIntensity(givenLevel, currentH, suma) * step # ilość wody jaka dolewa się do zbiornika w czasie danego kroku
        inputs.append(inputVolume / step)
        outputVolume = outputFactor * math.sqrt(currentH) * step # ilośc wody jaka wylała sie ze zbiornika w czasie tego kroku (zależna od pierwiastka z wysokosci wody w zbiorniku)
        result.append(currentH + ((inputVolume - outputVolume) / surfaceArea))

        steps.append(steps[len(steps) - 1] + step)

    df = pd.DataFrame({'x': steps, 'y': result})  # Wyświetlenie wykresu
    di = pd.DataFrame({'x': steps, 'y': inputs})  #
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


def getInputIntensity(target, current, suma): # algorytm wyliczający wartość sterowania (ilośc wływającej wody w jednostce czasu)
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

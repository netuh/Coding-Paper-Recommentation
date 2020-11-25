from flask import Blueprint, render_template
from flaskblog.models import *
from flaskblog.util import *
import json
from collections import Counter
import numpy as np

measurements = Blueprint('measurements', __name__)



@measurements.route("/measurements/index")
def index():
    measurements = Measurement.query.all()
    generalMeasurements = Counter()
    instrumentTimeCounter = Counter()
    instrumentSubjectiveCounter = Counter()
    instrumentCodeCounter = Counter()
    detailOtherCounter = Counter()
    for m in measurements:
        generalMeasurements.update([m.measurement_type])
        measurement_instrument = m.measurement_instruments if m.measurement_instruments else "Indeterminado"
        if (m.measurement_type == 'subjective'):
            instrumentSubjectiveCounter.update([measurement_instrument])
        if (m.measurement_type == 'time'):
            instrumentTimeCounter.update([measurement_instrument])
        if (m.measurement_type == 'code'):
            instrumentCodeCounter.update([measurement_instrument])
    generalChart = json.loads(create_plot_pie(generalMeasurements))
    instrumentSubChart = json.loads(create_plot_bar(instrumentSubjectiveCounter))
    instrumentTimeChart = json.loads(create_plot_bar(instrumentTimeCounter))
    instrumentCodeChart = json.loads(create_plot_bar(instrumentCodeCounter))
    generalChart[0]['values'] = [round((value * 100.0) / sum(generalChart[0]['values']), 2) for value in generalChart[0]['values']]

    return render_template('measurements/measurements_general.html', generalChart=generalChart[0],
                           instrumentSubChart=instrumentSubChart[0], instrumentTimeChart=instrumentTimeChart[0],
                           instrumentCodeChart=instrumentCodeChart[0])

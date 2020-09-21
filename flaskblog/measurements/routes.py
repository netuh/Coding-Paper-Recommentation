from flask import Blueprint, render_template
from flaskblog.models import *
from flaskblog.util import *
import json
from collections import Counter
import numpy as np

measurements = Blueprint('measurements', __name__)


@measurements.route("/measurements/index/")
def index():
    measurements = Measurement.query.all()
    generalMeasurements = Counter()
    instrumentTimeCounter = Counter()
    instrumentSubjectiveCounter = Counter()
    instrumentCodeCounter = Counter()
    detailOtherCounter = Counter()
    for m in measurements:
        generalMeasurements.update([m.measurement_type])
        if (m.measurement_type == 'SUBJECTIVE'):
            instrumentSubjectiveCounter.update([m.measurement_instruments])
        if (m.measurement_type == 'TIME'):
            instrumentTimeCounter.update([m.measurement_instruments])
        if (m.measurement_type == 'CODE'):
            instrumentCodeCounter.update([m.measurement_instruments])
        if (m.measurement_type == 'Others'):
            detailOtherCounter.update([m.measurement_details])
    generalChart = create_plot_pie(generalMeasurements)
    instrumentSubChart = create_plot_bar(instrumentSubjectiveCounter)
    instrumentTimeChart = create_plot_bar(instrumentTimeCounter)
    instrumentCodeChart = create_plot_bar(instrumentCodeCounter)
    detailOtherChart = create_plot_bar(detailOtherCounter)
    return render_template('measurements/measurements_general.html', generalChart=generalChart,
                           instrumentSubChart=instrumentSubChart, instrumentTimeChart=instrumentTimeChart,
                           instrumentCodeChart=instrumentCodeChart, detailOtherChart=detailOtherChart)


@measurements.route("/measurements/index/teste")
def index_teste():
    measurements = Measurement.query.all()
    generalMeasurements = Counter()
    instrumentTimeCounter = Counter()
    instrumentSubjectiveCounter = Counter()
    instrumentCodeCounter = Counter()
    detailOtherCounter = Counter()
    for m in measurements:
        generalMeasurements.update([m.measurement_type])
        if (m.measurement_type == 'SUBJECTIVE'):
            instrumentSubjectiveCounter.update([m.measurement_instruments])
        if (m.measurement_type == 'TIME'):
            instrumentTimeCounter.update([m.measurement_instruments])
        if (m.measurement_type == 'CODE'):
            instrumentCodeCounter.update([m.measurement_instruments])
        if (m.measurement_type == 'Others'):
            detailOtherCounter.update([m.measurement_details])
    generalChart = json.loads(create_plot_pie(generalMeasurements))
    instrumentSubChart = json.loads(create_plot_bar(instrumentSubjectiveCounter))
    instrumentTimeChart = json.loads(create_plot_bar(instrumentTimeCounter))
    instrumentCodeChart = json.loads(create_plot_bar(instrumentCodeCounter))
    detailOtherChart = json.loads(create_plot_bar(detailOtherCounter))
    return render_template('measurements/measurements_general_teste.html', generalChart=generalChart[0],
                           instrumentSubChart=instrumentSubChart[0], instrumentTimeChart=instrumentTimeChart[0],
                           instrumentCodeChart=instrumentCodeChart[0], detailOtherChart=detailOtherChart[0])

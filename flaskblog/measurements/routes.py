from flask import Blueprint, render_template
from flaskblog.models import *
from flaskblog.util import *

from collections import Counter
import numpy as np

measurements = Blueprint('measurements', __name__)


@measurements.route("/measurements/main/")
def main():
    measurements = Measurement.query.all()
    generalMeasurements = Counter()
    timeCounter = Counter()
    for m in measurements:
        generalMeasurements.update([m.measurement_type])
        if (m.measurement_type == 'SUBJECTIVE' and m.measurement_instruments):
            timeCounter.update(
                m.measurement_instruments.replace(" ", "").split(';'))
    generalChart = create_plot_bar(generalMeasurements)
    subjectiveChart = create_plot_bar(timeCounter)
    return render_template('measurements_general.html', plot=pie)


@measurements.route("/measurements/subjective/")
def subjectives():
    m_list = Measurement.query.filter_by(
        measurement_type=NatureOfDataSource.SUBJECTIVE)
    c = Counter()
    for m in m_list.all():
        if m.measurement_instruments:
            c.update(m.measurement_instruments.replace(" ", "").split(';'))
    bar = create_plot_bar(c)
    return render_template('subjective_measurements.html', plot=bar)


@measurements.route("/measurements/source_code/")
def objectives():
    m_list = Measurement.query.filter_by(
        measurement_type=NatureOfDataSource.SOURCE_CODE)
    c = Counter()
    for m in m_list.all():
        if m.measurement_instruments:
            c.update(m.measurement_instruments.replace(" ", "").split(';'))
    bar = create_plot_bar(c)
    return render_template('objective_measurements.html', plot=bar)


@measurements.route("/measurements/time/")
def time():
    m_list = Measurement.query.filter_by(
        measurement_type=NatureOfDataSource.TIME)
    c = Counter()
    for m in m_list.all():
        if m.measurement_instruments:
            c.update(m.measurement_instruments.replace(" ", "").split(';'))
    bar = create_plot_bar(c)
    return render_template('objective_measurements.html', plot=bar)

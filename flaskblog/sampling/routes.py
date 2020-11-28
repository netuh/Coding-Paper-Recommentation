from flask import Blueprint, render_template
from flaskblog.util import create_plot_bar
from flaskblog.models import *
from collections import Counter
import json

sampling = Blueprint('sampling', __name__)

@sampling.route("/sampling_main")
def sampling_main():
    recrutingStrategies = Recruting.query.all()

    redrutingMethodCounter = Counter()
    for strategy in recrutingStrategies:
        redrutingMethodCounter.update([strategy.recruiting_strategy])

    dic_classification = {}
    dic_classification['total'] = []
    dic_classification['mix'] = []
    dic_classification['professional_only'] = []
    dic_classification['student_only'] = []
    samples = Sampling.query.all()
    c = Counter()
    for a_profile in samples:
        classification, quantity = a_profile.sample_classification()
        dic_classification[classification].append(quantity)
        dic_classification['total'].append(quantity)
        for a_charac in a_profile.characteristics:
            c.update([a_charac.charac])

    sampleChart = json.loads(create_plot_violin(dic_classification))
    recruting = json.loads(create_plot_pie(redrutingMethodCounter))
    charac_plot = json.loads(create_plot_bar(c))
    recruting[0]['values'] = [round((value * 100.0) / sum(recruting[0]['values']), 2) for value in recruting[0]['values']]

    return render_template('sampling_pages/sampling_main.html', sampleChart=sampleChart, recruiting=recruting[0], charac_plot=charac_plot[0])
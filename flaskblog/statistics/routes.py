from flask import Blueprint, render_template
from flaskblog.models import *
from flaskblog.util import *

from collections import Counter
import numpy as np
import json

statistics = Blueprint('statistics', __name__)



@statistics.route("/statistics/index/")
def index():
    statistics = Statistics.query.all()
    statisticCounter = Counter()
    powerCounter = Counter()
    for s in statistics:
        string_statistics = s.statistic_details
        string_statistics = string_statistics.strip()
        string_statistics = string_statistics.replace("; ", ";")
        for aStat in string_statistics.split(";"):
            statisticCounter.update([aStat])
        if (s.has_power == 1):
            powerCounter.update(['yes'])
        else:
            powerCounter.update(['no'])
    statisticChart = json.loads(create_plot_bar(statisticCounter, False))
    powerChart = json.loads(create_plot_bar(powerCounter))
    return render_template('statistics/statistics_general.html', statisticChart=statisticChart[0],
                           powerChart=powerChart[0])

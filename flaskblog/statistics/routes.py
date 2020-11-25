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
        for aStat in s.statistic_details.split(";"):
            statisticCounter.update([aStat])
        powerCounter.update([s.has_power])
    statisticChart = json.loads(create_plot_bar(statisticCounter))
    powerChart = json.loads(create_plot_bar(powerCounter))
    return render_template('statistics/statistics_general.html', statisticChart=statisticChart[0],
                           powerChart=powerChart[0])

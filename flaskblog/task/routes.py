from flask import Blueprint, render_template
from flaskblog.util import create_plot_bar, create_plot_violin, create_plot_pie
from flaskblog.models import *
from collections import Counter
import json

task = Blueprint('task', __name__)


@task.route("/taskIndex")
def index():

    dic_classification = {}
    dic_classification['total_of_tasks'] = []
    dic_duration = {}
    dic_duration['total duration'] = []
    dic_duration['duration by task'] = []
    type_counter = Counter()

    tasks = Task.query.all()
    for a_task in tasks:
        if (a_task.quantity):
            dic_classification['total_of_tasks'].append(a_task.quantity)
        type_counter.update([a_task.task_type])

    experiments = Experiment.query.all()
    for a_experiment in experiments:
        if (a_experiment.median_task_duration):
            dic_duration['duration by task'].append(
                a_experiment.median_task_duration)
        if (a_experiment.median_experiment_duration):
            dic_duration['total duration'].append(
                a_experiment.median_experiment_duration)
    task_quantity = create_plot_violin(dic_classification, 'total of tasks')
    experiment_duration = create_plot_violin(
        dic_duration, 'total of tasks')
    type_counter = create_plot_pie(type_counter)
    print(task_quantity)
    print(experiment_duration)
    print(type_counter)
    return render_template('task_pages/tasks.html', task_quantity=task_quantity,
                           type_counter=type_counter, experiment_duration=experiment_duration)

@task.route("/taskIndex_teste")
def index_teste():

    dic_classification = {}
    dic_classification['total_of_tasks'] = []
    dic_duration = {}
    dic_duration['total duration'] = []
    dic_duration['duration by task'] = []
    type_counter = Counter()

    tasks = Task.query.all()
    for a_task in tasks:
        if (a_task.quantity):
            dic_classification['total_of_tasks'].append(a_task.quantity)
        type_counter.update([a_task.task_type])

    experiments = Experiment.query.all()
    for a_experiment in experiments:
        if (a_experiment.median_task_duration):
            dic_duration['duration by task'].append(
                a_experiment.median_task_duration)
        if (a_experiment.median_experiment_duration):
            dic_duration['total duration'].append(
                a_experiment.median_experiment_duration)

    task_quantity = json.loads(create_plot_violin(dic_classification, 'total of tasks'))
    experiment_duration = json.loads(create_plot_violin(
        dic_duration, 'total of tasks'))
    type_counter = json.loads(create_plot_pie(type_counter))
    type_counter[0]['values'] = [round((value * 100.0)/sum(type_counter[0]['values']),2) for value in type_counter[0]['values']]
    return render_template('task_pages/tasks_teste.html', task_quantity=task_quantity[0],
                           type_counter=type_counter[0], experiment_duration=experiment_duration)




@task.route("/taskDuration")
def taskDuration():
    counter_venues = Counter()
    counter_years = Counter()
    counter_institutions = Counter()
    counter_authors = Counter()
    publications = Publication.query.all()
    for pub in publications:
        counter_venues.update([pub.venue])
        counter_years.update([pub.year])
        counter_authors.update(map(str.strip, pub.authors.split(';')))

    bar_venues = create_plot_bar(counter_venues)
    bar_years = create_plot_bar(counter_years)
    return render_template('metadata.html', plot_venues=bar_venues, plot_years=bar_years,
                           most_common_authors=counter_authors.most_common(11))

from flask import render_template, request, Blueprint, redirect, url_for, session
from flaskblog.models import *
from flaskblog.finder.forms import SelectArticleForm
from flaskblog import db
import scholarly

finder = Blueprint('finder', __name__)


@finder.route("/select", methods=['GET', 'POST'])
def select():
    form = SelectArticleForm()

    design = ExperimentDesign.query.all()
    availableDesign = []
    for s in design:
        tupleWord = tuple((s.design_normalized, s.design_normalized))
        if (not tupleWord in availableDesign):
            availableDesign.append(tupleWord)
    form.designs.choices = availableDesign

    tasks = Task.query.all()
    taskType = []
    for s in tasks:
        for word in s.task_type.split(';'):
            word = word.replace(" ", "")
            tupleWord = tuple((word, word))
            if (not tupleWord in taskType):
                taskType.append(tupleWord)
    form.tasks.choices = taskType

    measurement = Measurement.query.all()
    availableMeasurement = []
    for s in measurement:
        tupleWord = tuple((s.measurement_type, s.measurement_type))
        if (not tupleWord in availableMeasurement):
            availableMeasurement.append(tupleWord)
    form.measurements.choices = availableMeasurement

    if form.validate_on_submit():
        session['tasks'] = form.tasks.data
        session['designs'] = form.designs.data
        session['measurements'] = form.measurements.data
        session['sample'] = form.sample.data.lower()
        return redirect(url_for('finder.list_articles', page=1))
    return render_template('finder/select.html', form=form)


@ finder.route("/list_articles")
def list_articles():
    design = session['designs']
    tasks = session['tasks']
    measurements = session['measurements']
    sample = session['sample']

    query_result = db.session.query(
        Publication
    ).join(
        Publication.experiments
    ).join(
        Experiment.design
    ).filter(ExperimentDesign.design_normalized == design)
    studies = query_result.all()
    if (measurements and len(measurements) > 0):
        studies = selectMeasurements(measurements, studies)
    if (tasks and len(tasks) > 0):
        studies = selectTask(tasks, studies)
    if (sample.lower() != 'all'):
        studies = selectSample(sample, studies)
    return render_template('research2.html', pubs=studies)


@ finder.route("/search")
def search():
    page = request.args.get('page', 1, type=int)
    pubs = Publication.query.order_by(
        Publication.year.desc()).paginate(page=page, per_page=5)
    return render_template('research.html', pubs=pubs)


@ finder.route("/details/<int:pub_id>")
def details(pub_id):
    pub = Publication.query.filter_by(pub_id=pub_id).first_or_404()
    search_query = scholarly.search_pubs_query(pub.title)
    paperData = next(search_query)
    title = paperData.bib['title']
    author = paperData.bib['author']
    abstract = paperData.bib['abstract']
    link = paperData.bib['url']
    year = pub.year
    venue = pub.venue
    return render_template('detail.html', title=title, author=author,
                           abstract=abstract, year=year, venue=venue,
                           link=link)


def selectMeasurements(measurements, studies):
    selected = []
    for aPub in studies:
        add = False
        for aExp in aPub.experiments:
            for aMeasu in aExp.measurements:
                if aMeasu.measurement_type in measurements:
                    add = True
        if (add):
            selected.append(aPub)
    return selected


def selectTask(tasks, studies):
    selected = []
    for aPub in studies:
        add = False
        for aExp in aPub.experiments:
            for aTask in aExp.tasks:
                if aTask.task_type in tasks:
                    add = True
        if (add):
            selected.append(aPub)
    return selected


def selectSample(sample, studies):
    selected = []
    for aPub in studies:
        add = False
        for aExp in aPub.experiments:
            for aSample in aExp.sample.profiles:
                if (sample in aSample.profile.lower()):
                    add = True
        if (add):
            selected.append(aPub)
    return selected

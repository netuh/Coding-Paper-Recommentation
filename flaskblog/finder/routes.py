from flask import render_template, request, Blueprint, redirect, url_for, session, jsonify, make_response
from flaskblog.finder.forms import SelectArticleForm
from flaskblog.models import *
from flaskblog import db
import scholarly
import json
from sqlalchemy import or_, and_, func, literal

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


@finder.route("/select_teste")
def select_teste():
    choices = {}

    design = ExperimentDesign.query.all()
    availableDesign = []
    for s in design:
        if not s.design_normalized in availableDesign:
            availableDesign.append(s.design_normalized)

    choices["designs"] = availableDesign

    tasks = Task.query.all()
    taskType = []
    for s in tasks:
        for word in s.task_type.split(';'):
            word = word.replace(" ", "")
            if not word in taskType:
                taskType.append(word)
    choices["tasks"] = taskType

    measurement = Measurement.query.all()
    availableMeasurement = []
    for s in measurement:
        if not s.measurement_type in availableMeasurement:
            availableMeasurement.append(s.measurement_type)
    choices["measurements"] = availableMeasurement

    choices["samples"] = ["Professional", "Student", "All"]
    return render_template('finder/select_characteristics_teste.html', choices=choices)


@finder.route("/list_articles")
def list_articles():
    design = session['designs']
    tasks = session['tasks']
    measurements = session['measurements']
    sample = session['sample']
    print(sample)

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
        print(sample)
        studies = selectSample(sample, studies)
    return render_template('research2.html', pubs=studies)


@finder.route("/search_characteristics_teste", methods=['POST'])
def search_characteristics_teste():
    search_characteristics_form = request.get_json()

    page = search_characteristics_form['page'] if 'page' in search_characteristics_form else 1

    query_result = db.session.query(
        Publication
    ).join(
        Publication.experiments
    ).join(
        Experiment.design
    ).join(

    ).filter(ExperimentDesign.design_normalized == search_characteristics_form['design'])

    studies = query_result.all()

    if search_characteristics_form['measurement']:
        studies = selectMeasurements(search_characteristics_form['measurement'], studies)
    if search_characteristics_form['task']:
        studies = selectTask(search_characteristics_form['task'], studies)
    if search_characteristics_form['sample'] and search_characteristics_form['sample'].lower() != 'all':
        print(search_characteristics_form['sample'])
        studies = selectSample(search_characteristics_form['sample'], studies)

    studies = [publication.pub_id for publication in studies]

    studies = db.session.query(
        Publication
    ).filter(Publication.pub_id.in_(studies)).paginate(per_page=7, page=page)

    studies = deserialize_papers(studies)

    res = make_response(json.dumps(studies), 200)
    return res


@finder.route("/search")
def search():
    page = request.args.get('page', 1, type=int)
    pubs = Publication.query.order_by(
        Publication.year.desc()).paginate(page=page, per_page=5)
    return render_template('research.html', pubs=pubs)


@finder.route("/details/<int:pub_id>")
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
            print(aExp.sample.exp_id)
            for aSample in aExp.sample.profiles:
                if (sample.lower() in aSample.profile.lower()):
                    print(aSample.profile.lower())
                    add = True
        if (add):
            selected.append(aPub)
    return selected


@finder.route("/finder/select_teste")
def index_teste():
    papers = Publication.query.all()
    authors = get_authors_papers(papers)
    titles = get_papers_title(papers)
    dict_authors_titles = dict.fromkeys(titles + authors)
    dict_authors_titles = json.dumps(dict_authors_titles)

    return render_template('finder/select_teste.html', dict_authors_titles=dict_authors_titles, )


def get_authors_papers(papers, authors=[]):
    for paper in papers:
        if (';' in paper.authors):
            authors.extend(paper.authors.split(';'))
        else:
            authors.append(paper.authors)
    return authors


def get_papers_title(papers, titles=[]):
    for paper in papers:
        titles.append(paper.title)
    return titles


@finder.route("/search_teste", methods=['GET'])
def search_teste():
    search = request.args.get('search', "", type=str)
    page = request.args.get('page', 1, type=int)
    search = "%{}%".format(search)
    publications = Publication.query.filter(
        or_(Publication.title.like(search), Publication.authors.like(search))).paginate(per_page=7, page=page)
    publications = deserialize_papers(publications)
    res = make_response(json.dumps(publications), 200)
    return res


def deserialize_papers(publications):
    if (publications):
        paper_author = []
        for publication in publications.items:
            paper_author.append(
                {"id": publication.pub_id, "name": publication.title, "authors": publication.authors})

        pages_conf = {"has_next": publications.has_next, "has_prev": publications.has_prev,
                      "next_num": publications.next_num, "page": publications.page,
                      "pages": [page for page in
                                publications.iter_pages(left_edge=1, right_edge=1, left_current=3, right_current=3)],
                      "prev_num": publications.prev_num}

        paper_pages = {"papers": paper_author, "page_conf": pages_conf}
        return paper_pages


@finder.route("/details_teste/<int:pub_id>")
def details_teste(pub_id):
    pub = Publication.query.filter_by(pub_id=pub_id).first_or_404()
    search_query = scholarly.search_pubs_query(pub.title)
    paperData = next(search_query)
    title = paperData.bib['title']
    author = paperData.bib['author']
    abstract = paperData.bib['abstract']
    link = paperData.bib['url']
    year = pub.year
    venue = pub.venue
    return render_template('detail_teste.html', title=title, author=author,
                           abstract=abstract, year=year, venue=venue,
                           link=link)

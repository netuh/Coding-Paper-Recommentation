from flask import render_template, request, Blueprint, redirect, url_for, session, jsonify, make_response
from flaskblog.models import *
from flaskblog import db
import json
from sqlalchemy import or_, and_, func, literal

finder = Blueprint('finder', __name__)


@finder.route("/select")
def select():
    choices = {}

    design = ExperimentDesign.query.all()
    availableDesign = ['All']
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

    choices["samples"] = ["All", "Professional", "Student"]
    return render_template('finder/select_characteristics.html', choices=choices)


@finder.route("/search_characteristics", methods=['POST'])
def search_characteristics():
    search_characteristics_form = request.get_json()

    page = search_characteristics_form['page'] if 'page' in search_characteristics_form else 1

    query_result = db.session.query(
        Publication
    ).join(
        Publication.experiments
    ).join(
        Experiment.design
    )
    if (search_characteristics_form['design'] != 'All'):
        query_result = query_result.filter(ExperimentDesign.design_normalized == search_characteristics_form['design'])

    studies = query_result.all()

    if search_characteristics_form['measurement']:
        studies = selectMeasurements(search_characteristics_form['measurement'], studies)
    if search_characteristics_form['task']:
        studies = selectTask(search_characteristics_form['task'], studies)
    if search_characteristics_form['sample'] and search_characteristics_form['sample'].lower() != 'all':
        studies = selectSample(search_characteristics_form['sample'], studies)

    studies = [publication.pub_id for publication in studies]

    studies = db.session.query(
        Publication
    ).filter(Publication.pub_id.in_(studies)).paginate(per_page=7, page=page)

    studies = deserialize_papers(studies)

    res = make_response(json.dumps(studies), 200)
    return res


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
                if (sample.lower() in aSample.profile.lower()):
                    add = True
        if (add):
            selected.append(aPub)
    return selected


@finder.route("/finder/select")
def index():
    papers = Publication.query.all()
    authors = get_authors_papers(papers)
    titles = get_papers_title(papers)
    dict_authors_titles = dict.fromkeys(titles + authors)
    dict_authors_titles = json.dumps(dict_authors_titles)

    return render_template('finder/select.html', dict_authors_titles=dict_authors_titles, )


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


@finder.route("/search", methods=['GET'])
def search():
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


@finder.route("/details/<int:pub_id>")
def details(pub_id):
    pub = Publication.query.filter_by(pub_id=pub_id).first_or_404()
    paperData = google_scholar_grap("{0} {1}".format(pub.title, pub.authors))
    title = paperData['title']
    author = paperData['authors']
    abstract = paperData['abstract']
    link = paperData['url']
    year = pub.year
    venue = pub.venue
    return render_template('detail.html', title=title, author=author,
                           abstract=abstract, year=year, venue=venue,
                           link=link)

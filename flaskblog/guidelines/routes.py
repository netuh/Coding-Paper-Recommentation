from flask import Blueprint, render_template
from flaskblog.models import Publication, Guideline

import scholarly
guidelines = Blueprint('guidelines', __name__)


@guidelines.route("/guidelines")
def all():
    guidelines = Guideline.query.all()
    return render_template('guidelines.html', guidelines=guidelines)

@guidelines.route("/guidelines_test")
def all_test():
    guidelines = Guideline.query.all()
    return render_template('guidelines_test.html', guidelines=guidelines)


@guidelines.route("/guideline/<int:guide_id>/")
def guide(guide_id):
    g = Guideline.query.get_or_404(guide_id)
    search_query = scholarly.search_pubs_query(g.title)
    paperData = next(search_query)
    title = paperData.bib['title']
    author = paperData.bib['author']
    abstract = paperData.bib['abstract']
    link = paperData.bib['url']
    return render_template('guideline_details.html', title=title, author=author,
                           abstract=abstract, link=link, references=g.referenced_by)

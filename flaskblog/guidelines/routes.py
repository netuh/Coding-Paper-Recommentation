from flask import Blueprint, render_template
from flaskblog.models import Guideline
from flaskblog.util import google_scholar_grap
from scholarly import scholarly, ProxyGenerator

guidelines = Blueprint('guidelines', __name__)


def sort_guidelines_qtd(guideline):
    tamanho = len(guideline.referenced_by)
    return tamanho


@guidelines.route("/guidelines")
def all():
    guidelines = Guideline.query.all()
    guidelines.sort(reverse=True, key=sort_guidelines_qtd)
    return render_template('guidelines.html', guidelines=guidelines)


@guidelines.route("/guideline/<int:guide_id>/")
def guide(guide_id):
    g = Guideline.query.get_or_404(guide_id)
    pg = ProxyGenerator()
    pg.SingleProxy(http="http://scraperapi:8fccbfbc3c3d3d708cb9691af4099a2a@proxy-server.scraperapi.com:8001",
                   https="http://scraperapi:8fccbfbc3c3d3d708cb9691af4099a2a@proxy-server.scraperapi.com:8001")
    scholarly.use_proxy(pg)
    paperData = scholarly.search_single_pub("{0} {1}".format(g.title, g.authors))
    # paperData = google_scholar_grap("{0} {1}".format(g.title, g.authors))
    title = paperData.bib['title']
    author = paperData.bib['author']
    abstract = paperData.bib['abstract']
    link = paperData.bib['url']
    return render_template('guideline_details.html', title=title, author=author,
                           abstract=abstract, link=link, references=g.referenced_by)

from flask import Blueprint, render_template
from flaskblog.models import Guideline

from scholarly import scholarly, ProxyGenerator
guidelines = Blueprint('guidelines', __name__)

def sort_guidelines_qtd(guideline):
    tamanho = len(guideline.referenced_by)
    return tamanho



@guidelines.route("/guidelines")
def all():
    guidelines = Guideline.query.all()
    guidelines.sort(reverse=True,key=sort_guidelines_qtd)
    return render_template('guidelines.html', guidelines=guidelines)


@guidelines.route("/guideline/<int:guide_id>/")
def guide(guide_id):
    g = Guideline.query.get_or_404(guide_id)
    pg = ProxyGenerator()
    scholarly.use_proxy(pg)
    search_query = scholarly.search_pubs(g.title)
    paperData = next(search_query)
    title = paperData.bib['title']
    author = paperData.bib['author']
    abstract = paperData.bib['abstract']
    link = paperData.bib['url']
    return render_template('guideline_details.html', title=title, author=author,
                           abstract=abstract, link=link, references=g.referenced_by)

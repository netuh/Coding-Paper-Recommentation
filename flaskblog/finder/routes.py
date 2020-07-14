from flask import render_template, request, Blueprint
from flaskblog.models import Publication
import scholarly

finder = Blueprint('finder', __name__)


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

from flask import Blueprint, render_template
from flaskblog.util import create_plot_bar
from flaskblog.models import Publication
from collections import Counter
import json

data_vizualization = Blueprint('data_vizualization', __name__)


@data_vizualization.route("/metadata")
def metadata():
    counter_venues = Counter()
    counter_years = Counter()
    counter_authors = Counter()
    publications = Publication.query.all()
    for pub in publications:
        counter_venues.update([pub.venue])
        counter_years.update([pub.year])
        counter_authors.update(map(str.strip, pub.authors.split(';')))

    bar_venues = json.loads(create_plot_bar(counter_venues))
    bar_years = json.loads(create_plot_bar(counter_years))

    return render_template('metadata.html', plot_venues=bar_venues[0], plot_years=bar_years[0],
                           most_common_authors=counter_authors.most_common(20))
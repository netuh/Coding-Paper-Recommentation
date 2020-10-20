from flask import Blueprint, render_template
from flaskblog.util import create_plot_bar
from flaskblog.models import *
from collections import Counter

design = Blueprint('design', __name__)


@design.route("/designIndex")
def index():
    desings = ExperimentDesign.query.all()
    designCounter = Counter()
    explicitDesignCounter = Counter()
    treatmentCounter = Counter()
    for a_desing in desings:
        # designCounter.update([a_desing.design_description])
        explicitDesignCounter.update([a_desing.design_normalized])
        if (a_desing.is_explicity_design == 1):
            designCounter.update([a_desing.design_description])
        treatmentCounter.update([a_desing.treatment_quantity])
    all_design_chart = create_plot_bar(designCounter)
    explicited_chart = create_plot_bar(explicitDesignCounter)
    treatment_chart = create_plot_bar(treatmentCounter)
    return render_template('design_pages/designs.html', all_design=all_design_chart, explicited_design=explicited_chart, treatment=treatment_chart)

@design.route("/designIndex_teste")
def index_teste():
    desings = ExperimentDesign.query.all()
    designCounter = Counter()
    explicitDesignCounter = Counter()
    treatmentCounter = Counter()
    for a_desing in desings:
        designCounter.update([a_desing.design_description])
        if (a_desing.is_explicity_design == 1):
            explicitDesignCounter.update([a_desing.design_description])
        treatmentCounter.update([a_desing.treatment_quantity])
    all_design_chart = json.loads(create_plot_bar(designCounter))
    explicited_chart = json.loads(create_plot_bar(explicitDesignCounter))
    treatment_chart = json.loads(create_plot_bar(treatmentCounter))

    print(all_design_chart[0])
    print(explicited_chart[0])
    print(treatment_chart[0])

    return render_template('design_pages/designs_teste.html', all_design=all_design_chart[0], explicited_design=explicited_chart[0], treatment=treatment_chart[0])


@design.route("/detailDesign")
def detailDesign():
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


@design.route("/detailFactor")
def detailFactor():
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

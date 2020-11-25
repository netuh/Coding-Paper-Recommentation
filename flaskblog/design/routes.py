from flask import Blueprint, render_template
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
        explicitDesignCounter.update([a_desing.design_normalized])
        if (a_desing.is_explicity_design == 1):
            designCounter.update([a_desing.design_description])
        treatmentCounter.update([a_desing.treatment_quantity])
    all_design_chart = json.loads(create_plot_bar(designCounter))
    explicited_chart = json.loads(create_plot_bar(explicitDesignCounter))
    treatment_chart = json.loads(create_plot_bar(treatmentCounter))

    return render_template('design_pages/designs.html', all_design=all_design_chart[0], explicited_design=explicited_chart[0], treatment=treatment_chart[0])

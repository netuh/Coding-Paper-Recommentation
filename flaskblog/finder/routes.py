from flask import render_template, request, Blueprint
from flaskblog.models import Publication, Sampling
from flaskblog.finder.forms import SelectArticleForm
from flaskblog import db
import scholarly

finder = Blueprint('finder', __name__)


@finder.route("/finder/select", methods=['GET', 'POST'])
def index():
    form = SelectArticleForm()

    samplings = Sampling.query.all()
    max_value = -1
    min_value = 600
    for s in samplings:
        if (s.sampleQuantity() > max_value):
            max_value = s.sampleQuantity()
        if (s.sampleQuantity() < min_value):
            min_value = s.sampleQuantity()

    print(min_value)
    print(max_value)
    design_list = [('-None-', '-None-')]
    form.designs.choices = design_list

    task_type_list = ['a', 'b', 'c']
    form.performed_tasks.choices = task_type_list

    nature_of_data_list = ['a', 'b', 'c']
    form.nature_of_data.choices = nature_of_data_list

    duration_list = [('-None-', '-None-')]
    form.duration.choices = duration_list

    profile_list = []
    form.profile_type.choices = profile_list

    recruitment_list = []
    form.recruting_type.choices = recruitment_list
    # if form.validate_on_submit():
    #     print(f'select={form.lab_settings.data}')
    #     data = {}
    #     data['min'] = form.sample_size_min.data
    #     data['max'] = form.sample_size_max.data
    #     if form.lab_settings.data:
    #         data['lab'] = True
    #     if form.recruting_type.data:
    #         data['recruting'] = form.recruting_type.data
    #     if form.nature_of_data.data:
    #         data['nature_of_data'] = form.nature_of_data.data
    #     if form.performed_tasks.data:
    #         data['performed_tasks'] = form.performed_tasks.data
    #     if form.profile_type.data:
    #         data['profile_type'] = form.profile_type.data

    #     if form.designs.data != '-None-':
    #         data['design'] = form.designs.data
    #     if form.duration.data != '-None-':
    #         data['duration'] = form.duration.data
    #     messages = json.dumps(data)
    #     return redirect(url_for('articles.list_articles', page=1, messages=messages))
    return render_template('finder/select.html', form=form)


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
from flaskblog.models import *
from flaskblog import create_app
from flaskblog import db

app = create_app()

guides = {}


def createGuidelines():
    createAGuideline('Experimentation in Software Engineering',
                     'Wohlin et al.')
    createAGuideline('Design and Analysis of Experiments',
                     'Montgomery et al.')
    createAGuideline('Repeatable software engineering experiments for comparing defect-detection techniques',
                     'Lott and Rombach')

    for g in guides.values():
        db.session.add(g)
    db.session.commit()


def createAGuideline(newTitle, newAuthors):
    g = Guideline(title=newTitle, authors=newAuthors)
    guides[newAuthors] = g


def newExperiment(newTitle, newYear, newVenue, newAuthors, guidelines, newSettings):
    p = Publication(title=newTitle, year=newYear, venue=newVenue,
                    authors=newAuthors)
    e = Experiment(settings=newSettings)
    for g in guidelines:
        p.guidelines.append(guides[g])
    p.experiments.append(e)
    db.session.add(p)
    db.session.add(e)
    return e


def addExperiment(experiment, newSettings):
    e = Experiment(settings=newSettings)
    experiment.exp_pub.append(e)

    db.session.add(e)
    return e


def addTask(newTaskType, newQuantity, experiment):
    t = Task(task_type=newTaskType, quantity=newQuantity)
    t.task_parent = experiment
    db.session.add(t)


def setExperimentDesign(newDesign, explicity, treatmentQuantity, experiment):
    d = ExperimentDesign(design_description=newDesign, is_explicity_design=explicity,
                         treatment_quantity=treatmentQuantity)
    experiment.design = d
    db.session.add(d)


def createSampling(strategy, experiment):
    s = Sampling()
    s.exp = experiment
    r = Recruting(recruiting_strategy=strategy, parent_recru=s)
    db.session.add(s)
    db.session.add(r)
    return s


def addProfile(newProfile, newQuantity, sample):
    sp = SamplingProfile(profile=newProfile,
                         quantity=newQuantity, parent_profile=sample)
    db.session.add(sp)


def addCharacteristic(newCharac, sample):
    sc = SamplingCharacteristic(charac=newCharac, parent_charac=sample)
    db.session.add(sc)


def addMeasuriment(experiment, newMeasure='TIME', instrument=None, details=None):
    m = Measurement(measurement_type=newMeasure)
    if (instrument):
        m.measurement_instruments = instrument
    if (details):
        m.measurement_details = details
    experiment.measurements.append(m)
    db.session.add(m)


def createStatistics(experiment, hasPower=0, details=None):
    s = Statistics(has_power=hasPower, statistic_details=details)
    s.exp = experiment
    db.session.add(s)


def createPaper1():
    e = newExperiment('Answering software evolution questions: An empirical evaluation', 2013, 'IST',
                      'Lile Hattori; Marco D’Ambros; Michele Lanza; Mircea Lungu',
                      ['Wohlin et al.'], 'Laboratory')
    e.median_experiment_duration = 0.5
    addTask(newTaskType='COMPREENSION', newQuantity=6, experiment=e)
    setExperimentDesign(newDesign='between-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Posgrad Student', newQuantity=44, sample=s)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='sex', sample=s)
    addCharacteristic(newCharac='nationality', sample=s)
    addCharacteristic(newCharac='Level of experience', sample=s)
    addCharacteristic(newCharac='Years of experience', sample=s)
    addCharacteristic(newCharac='Linux experience', sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='paper form')
    createStatistics(e, 0, 't-test; Mann–Whitney')


def createPaper2():
    e = newExperiment('The impact of Software Testing education on code reliability: An empirical assessment', 2018, 'JSS',
                      'Otávio Augusto Lazzarini Lemos; Fábio Fagundes Silveira; Fabiano Cutigi Ferrari; Alessandro Garcia',
                      ['Montgomery et al.'], 'Laboratory')
    e.median_task_duration = 2
    addTask(newTaskType='CONSTRUCTION', newQuantity=4, experiment=e)
    setExperimentDesign(newDesign='cross-over design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    s = createSampling('Not Clear', e)
    addProfile(newProfile='GradStudent', newQuantity=60, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='paper form')
    createStatistics(e, 0, 't-test; Shapiro-Wilk')


def createPaper3():
    e = newExperiment('A replicated experiment for evaluating the effectiveness of pairing practice in PSP education', 2019, 'JSS',
                      'Guoping Rong; He Zhang; Bohan Liu; Qi Shan; Dong Shao',
                      [], 'Laboratory')
    e.median_task_duration = 2
    addTask(newTaskType='CONSTRUCTION', newQuantity=4, experiment=e)
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    s = createSampling('Not Clear', e)
    addProfile(newProfile='GradStudent', newQuantity=120, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='QUESTION', instrument='form')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='Experimenter and log')
    addMeasuriment(experiment=e, newMeasure='Others',
                   details='Number Of Errors')
    addMeasuriment(experiment=e, newMeasure='Others', details='grade')
    createStatistics(e, 0, 'Wilcoxon')


def createPaper4():
    e = newExperiment('On some end-user programming constructs and their understandability', 2018, 'JSS',
                      'M Mackowiak,; J Nawrocki; M Ochodek',
                      [], 'Laboratory')
    e.median_experiment_duration = 0.1
    addTask(newTaskType='comprehension', newQuantity=1, experiment=e)
    addTask(newTaskType='others', newQuantity=1, experiment=e)
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=1, treatmentQuantity=1, experiment=e)
    s = createSampling('Not Clear', e)
    addProfile(newProfile='Undergrad Student', newQuantity=114, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')
    createStatistics(e, 1, 'Mann-Whitney; Wilcoxon')


def createPaper5():
    e = newExperiment('A controlled experiment in assessing and estimating software maintenance tasks', 2018, 'JSS',
                      'M Mackowiak,; J Nawrocki; M Ochodek',
                      [], 'Laboratory')
    e.median_experiment_duration = 0.1
    addTask(newTaskType='maintenance', newQuantity=17, experiment=e)
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=1, treatmentQuantity=3, experiment=e)
    s = createSampling('Not Clear', e)
    addProfile(newProfile='Undergradstudent', newQuantity=23, sample=s)
    addProfile(newProfile='Gradstudent', newQuantity=1, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='paper form')
    createStatistics(e, 1, 'Mann-Whitney')


def createPaper6():
    e = newExperiment('Impact of test-driven development on productivity, code and tests: A controlled experiment', 2011, 'IST',
                      'M Pancur; M Ciglaric',
                      ['Wohlin et al.', 'Lott and Rombach'], 'Laboratory and Home')
    e.median_experiment_duration = 35
    e.median_task_duration = 4
    addTask(newTaskType='CONSTRUCTION', newQuantity=27, experiment=e)
    setExperimentDesign(newDesign='standard one factor and two treatments',
                        explicity=1, treatmentQuantity=2, experiment=e)
    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Gradstudent', newQuantity=34, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')
    createStatistics(e, 1, 'Kolmogorov–Smirnov; Shapiro–Wilk; Mann-Whitney')


def createPaper7():
    e = newExperiment('Evaluating the productivity of a reference-based programming approach: A controlled experiment', 2014, 'IST',
                      'A Sturm; O Kramer',
                      [], 'Laboratory')
    e.median_experiment_duration = 0.1
    e.median_task_duration = 9
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)
    setExperimentDesign(newDesign='standard one factor and two treatments',
                        explicity=1, treatmentQuantity=2, experiment=e)
    s = createSampling('Extra grade', e)
    addProfile(newProfile='Gradstudent', newQuantity=50, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='paper form')
    createStatistics(e, 0, 'Mann-Whitney')


def createPaper8():
    e = newExperiment('Are team personality and climate related to satisfaction and software quality? Aggregating results from a twice replicated experiment', 2015, 'IST',
                      'Acuña, S. T.; Gómez, M. N.; Hannay, J. E.; Juristo, N.; Pfahl, D.',
                      [], 'Laboratory')
    e.median_experiment_duration = 100
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    createStatistics(e, 1, 'Meta-analyses of correlations')

    s = createSampling('Not Clear', e)
    addProfile(newProfile='Gradstudent', newQuantity=105, sample=s)


def createPaper9():
    e = newExperiment('Towards an operationalization of test-driven development skills: An industrial empirical study', 2015, 'IST',
                      'Fucci, D.; Turhan, B.; Juristo, N.; Dieste, O.; Tosun-Misirli, A.; Oivo, M.',
                      [], 'Company')
    e.median_experiment_duration = 5
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=1, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=3, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    createStatistics(e, 1, 'ANOVA')

    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Professionals', newQuantity=30, sample=s)


def createPaper10():
    e = newExperiment('Tester interactivity makes a difference in search-based software testing: A controlled experiment', 2016, 'IST',
                      'Marculescu, B.; Poulding, S.; Feldt, R.; Petersen, K.; Torkar, R. ',
                      [], 'Company')
    e.median_task_duration = 0.75
    setExperimentDesign(newDesign='crossover design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='TEST', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='questionaire')
    addMeasuriment(experiment=e, newMeasure='CODE', details='test cases')
    createStatistics(e, 1, 'Mann-Whitney')

    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Gradstudent', newQuantity=58, sample=s)


def createPaper11():
    e = newExperiment('Comparing the comprehensibility of requirements models: An experiment replication', 2018, 'IST',
                      'Siqueira FL',
                      ['Wohlin et al.'], 'Laboratory')
    e.median_task_duration = 1.5
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=3, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='questionaire')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='Experimenter')

    createStatistics(e, 0, 'Mann-Whitney')

    s = createSampling('Part of Course', e)
    addProfile(newProfile='Gradstudent', newQuantity=32, sample=s)


def createPaper12():
    e = newExperiment('Live programming in practice: A controlled experiment on state machines for robotic behaviors', 2018, 'IST',
                      'Campusano, M.; Fabry, J.; Bergel, A.',
                      [], 'Laboratory')
    # experiment 1
    e.median_task_duration = 4
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')
    createStatistics(e, 0, 'Mann-Whitney')

    s = createSampling('Not Clear', e)
    addProfile(newProfile='Gradstudent', newQuantity=2, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=8, sample=s)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='Scholarity', sample=s)
    addCharacteristic(newCharac='tool expertize', sample=s)

    # experiment 2
    e2 = addExperimet(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e2)
    addTask(newTaskType='CONSTRUCTION', newQuantity=3, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e2, newMeasure='TIME')
    createStatistics(e2, 0, 'Mann-Whitney')

    s2 = createSampling('Not Clear', e)
    addProfile(newProfile='Gradstudent', newQuantity=2, sample=s2)
    addProfile(newProfile='Undergradstudent', newQuantity=8, sample=s2)


def createPaper13():
    e = newExperiment('Using cognitive dimensions to evaluate the usability of security APIs: An empirical investigation', 2019, 'IST',
                      'Wijayarathna, C.; Arachchilage, N. A. G. ',
                      ['Wohlin et al.'], 'Home')
    e.median_task_duration = 1.5
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=1, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, '')

    s = createSampling('Reward', e)
    addCharacteristic(newCharac='development experience', sample=s)
    addCharacteristic(newCharac='Java experience', sample=s)
    addCharacteristic(newCharac='Hour Java', sample=s)
    addCharacteristic(newCharac='API Experience', sample=s)
    addProfile(newProfile='Professionals', newQuantity=40, sample=s)


def createPaper14():
    e = newExperiment('Using cognitive dimensions to evaluate the usability of security APIs: An empirical investigation', 2019, 'IST',
                      'Wijayarathna, C.; Arachchilage, N. A. G. ',
                      ['Wohlin et al.'], 'Home')
    e.median_task_duration = 1.5
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=1, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, '')

    s = createSampling('Reward', e)
    addCharacteristic(newCharac='development experience', sample=s)
    addCharacteristic(newCharac='Java experience', sample=s)
    addCharacteristic(newCharac='Hour Java', sample=s)
    addCharacteristic(newCharac='API Experience', sample=s)
    addProfile(newProfile='Professionals', newQuantity=40, sample=s)


@ app.before_first_request
def before_first_request_func():
    db.drop_all()
    db.create_all()
    createGuidelines()
    createPaper1()
    createPaper2()
    createPaper3()
    createPaper4()
    createPaper5()
    createPaper6()
    createPaper7()
    createPaper8()
    createPaper9()
    createPaper10()
    createPaper11()
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)

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
    createAGuideline('Basics of software engineering experimentation',
                     'Juristo and Moreno')
    createAGuideline('Improving Quality through Planned Experimentation.',
                     'R. Moen, T. Nolan, and L. Provost')
    createAGuideline('Reporting experiments in software engineering',
                     'Jedlitschka et al.')
    createAGuideline('Desmet: a method for evaluating software engineering methods and tools',
                     'Kitchenham, B.')
    createAGuideline('Qualitative Methods in Empirical Studies of Software Engineering',
                     'Seaman, C.B.')


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
    experiment.exp_pub.experiments.append(e)

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
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')
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
    addTask(newTaskType='COMPREENSION', newQuantity=1, experiment=e)
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
    addTask(newTaskType='MAINTENANCE', newQuantity=17, experiment=e)
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
                   instrument='form')
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
                   instrument='form')
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
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e2)
    addTask(newTaskType='CONSTRUCTION', newQuantity=3, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e2, newMeasure='TIME')
    createStatistics(e2, 0, 'Mann-Whitney')

    s2 = createSampling('Not Clear', e2)
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
    e = newExperiment('The impact of test-first programming on branch coverage and mutation score indicator of unit tests: An experiment', 2010, 'IST',
                      'Madeyski L.',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 5
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='TEST', newQuantity=1, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=6, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='repository')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='paper form')

    createStatistics(
        e, 1, 'Kolmogorov–Smirnov; Shapiro–Wilk; Mahalanobis distance;' +
        ' Levene’s test of homogeneity; Test of Equality of Covariance Matrices; MANCOVA')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='programming experience', sample=s)
    addCharacteristic(newCharac='JUnit experience', sample=s)
    addCharacteristic(newCharac='Larger program in JAVA', sample=s)
    addProfile(newProfile='GradStudent', newQuantity=19, sample=s)


def createPaper15():
    e = newExperiment('Combining Functional and Imperative Programming for Multicore Software: An Empirical Study Evaluating Scala and Java', 2012, 'ICSE',
                      'Pankratius, V.; Schmidt, F.; Garretón, G.',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    e.median_experiment_duration = 28
    setExperimentDesign(newDesign='counterbalanced within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='upload')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='form')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 1, 'Wilcoxon')

    s = createSampling('Not Clear', e)
    addProfile(newProfile='GradStudent', newQuantity=13, sample=s)


def createPaper16():
    e = newExperiment('An Empirical Study on the Developers’ Perception of Software Coupling', 2012, 'ICSE',
                      'Bavota, G.; Dit, B.; Oliveto, R.; Di Penta, M.; Poshyvanyk, D.; De Lucia, A.',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=1, treatmentQuantity=4, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')

    createStatistics(e, 1, 'Mann-Whitney test')

    s = createSampling('Not Clear', e)
    addProfile(newProfile='GradStudent', newQuantity=49, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=10, sample=s)
    addProfile(newProfile='Professionals', newQuantity=14, sample=s)


def createPaper17():
    e = newExperiment('Recommending Source Code for Use in Rapid Software Prototypes', 2012, 'ICSE',
                      'McMillan, C.; Hariri, N.; Poshyvanyk, D.; Cleland-Huang, J.; Mobasher, B.',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Cross-Validation Design',
                        explicity=1, treatmentQuantity=4, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=12, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')

    createStatistics(e, 0, 'ANOVA; t-test')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Industry experience', sample=s)
    addCharacteristic(newCharac='Java experience', sample=s)
    addProfile(newProfile='GradStudent', newQuantity=28, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=3, sample=s)


def createPaper18():
    e = newExperiment('Improving Feature Location Practice with Multi-faceted Interactive Exploration', 2013, 'ICSE',
                      'Wang, J.; Peng, X.; Xing, Z.; Zhao, W. ',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='screen recorder')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='screen recorder')

    createStatistics(e, 0, 't-test')

    s = createSampling('Not Clear', e)
    addProfile(newProfile='GradStudent', newQuantity=13, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=7, sample=s)


def createPaper19():
    e = newExperiment('The Effect of Noise on Software Engineers’ Performance', 2018, 'ESEM',
                      'Romano, S.; Scanniello, G.; Fucci, D.; Juristo, N.; Turhan, B.',
                      ['Juristo and Moreno', 'Wohlin et al.'], 'Laboratory')
    e.median_task_duration = 0.5
    e.median_experiment_duration = 0.1
    setExperimentDesign(newDesign='AB/BA crossover design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')

    createStatistics(e, 1, 'Mann-Whitney; t-test; Shapiro test')

    s = createSampling('Extra Grade', e)
    addProfile(newProfile='Undergradstudent', newQuantity=55, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e2)
    addTask(newTaskType='MAINTENANCE', newQuantity=2, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='CODE')
    createStatistics(e2, 1, 'Mann-Whitney; Shapiro test')

    s2 = createSampling('Extra Grade', e2)
    addProfile(newProfile='Undergradstudent', newQuantity=42, sample=s2)


def createPaper20():
    e = newExperiment('Developer Reading Behavior While Summarizing Java Methods: Size and Context Matters', 2019, 'ICSE',
                      'Abid, N. J.; Sharif, B.; Dragan, N.; Alrasheed, H.; Maletic, J. I. ',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=1, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=23, experiment=e)

    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='eye traker')
    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='Eclipse iTrace')

    createStatistics(e, 1, 'wilcoxon test, Bonferroni p-value correction')

    s = createSampling('Not Clear', e)
    addProfile(newProfile='GradStudent', newQuantity=3, sample=s)
    addProfile(newProfile='Student', newQuantity=13, sample=s)
    addProfile(newProfile='Professionals', newQuantity=2, sample=s)


def createPaper21():
    e = newExperiment('Debugging for Reactive Programming', 2016, 'ICSE',
                      'Salvaneschi, G.; Mezini, M.',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='between-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='DEGUGGING', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Mann-Whitney')

    s = createSampling('Not Clear', e)
    addProfile(newProfile='Undergradstudent', newQuantity=18, sample=s)


def createPaper22():
    e = newExperiment('The Effect of Poor Source Code Lexicon and Readability on Developers’ Cognitive Load', 2018, 'ICSE',
                      'Fakhoury, S.; Ma, Y.; Arnaoudova, V.; Adesope, O. ',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=4, experiment=e)
    addTask(newTaskType='DEGUGGING', newQuantity=1, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='eye traker')
    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='Brain Image')

    createStatistics(e, 1, 'Wilcoxon')

    s = createSampling('Reward', e)
    addProfile(newProfile='Professionals', newQuantity=15, sample=s)


def createPaper23():
    e = newExperiment('A Controlled Experiment for Program Comprehension through Trace Visualization', 2018, 'ICSE',
                      'Cornelissen, B.; Zaidman, A.; van Deursen, A.',
                      [], 'Laboratory')
    e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=4, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=8, experiment=e)

    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='eye traker')
    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='Brain Image')

    createStatistics(e, 0, 'Kolmogorov-Smirnov; Levene test; t-test')

    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Gradstudent', newQuantity=26, sample=s)
    addProfile(newProfile='Professionals', newQuantity=8, sample=s)


def createPaper24():
    e = newExperiment('A Controlled Experiment for Evaluating the Impact of Coupling on the Maintainability of Service-Oriented Software', 2010, 'TSE',
                      'Cornelissen, B.; Zaidman, A.; van Deursen, A.',
                      ['R. Moen, T. Nolan, and L. Provost'], 'Laboratory')
    e.median_task_duration = 3
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='incomplete within-subjects design',
                        explicity=1, treatmentQuantity=4, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='Experimenter')

    createStatistics(
        e, 1, 'Shapiro-Wilk, ANOVA, t-test, Wilcoxon; Kruskal Wallis test; Fishers Least-Significant Difference (LSD) mean comparison test')

    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Gradstudent', newQuantity=5, sample=s)


def createPaper25():
    e = newExperiment('Improving Source Code Lexicon via Traceability and Information Retrieval', 2010, 'TSE',
                      'De Lucia, A.; Di Penta, M.; Oliveto, R.',
                      [], 'Laboratory')
    e.median_task_duration = 2
    e.median_experiment_duration = 0.1
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='form')

    createStatistics(e, 1, 'Wilk-Shapiro; Mann-Whitney')

    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Gradstudent', newQuantity=16, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e2)
    e2.median_task_duration = 2
    addTask(newTaskType='MAINTENANCE', newQuantity=2, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='CODE')
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE',
                   instrument='form')
    createStatistics(e2, 1, 'Mann-Whitney; Shapiro test')

    s2 = createSampling('Extra Grade', e2)
    addProfile(newProfile='Undergradstudent', newQuantity=20, sample=s2)


def createPaper26():
    e = newExperiment('Preserving Aspects via Automation: a Maintainability Study', 2011, 'ESEM',
                      'Hovsepyan, A., Scandariato, R., Van Baelen, S., Joosen, W., & Demeyer, S.',
                      [], 'Laboratory')
    e.median_task_duration = 3
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='tool')

    createStatistics(e, 1, 'Shapiro-Wilk test; t-test')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='Programming experience', sample=s)
    addCharacteristic(newCharac='Java experience', sample=s)
    addCharacteristic(newCharac='UML experience', sample=s)
    addProfile(newProfile='Gradstudent', newQuantity=17, sample=s)


def createPaper27():
    e = newExperiment('A Replicated Experiment on the Effectiveness of Test-first Development', 2013, 'ESEM',
                      'Fucci, D.; Turhan, B. ',
                      ['Juristo and Moreno'], 'Laboratory')
    e.median_task_duration = 3
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 1, 'Lilliefors test; Mann-Whitney; ANCOVA')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='OO experience', sample=s)
    addCharacteristic(newCharac='JUnit experience', sample=s)
    addCharacteristic(newCharac='TDD experience', sample=s)
    addCharacteristic(newCharac='Eclipse experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=33, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=25, sample=s)


def createPaper28():
    e = newExperiment('Refactoring Inspection Support for Manual Refactoring Edits', 2017, 'TSE',
                      'Alves, E. L.; Song, M.; Massoni, T.; Machado, P. D.; Kim, M.',
                      [], 'Laboratory')
    e.median_task_duration = 3
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='INSPECTION', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Chi-squared Proportion Tests')

    s = createSampling('Voluntiers', e)

    addProfile(newProfile='Professionals', newQuantity=15, sample=s)


def createPaper29():
    e = newExperiment('A Comparison of Program Comprehension Strategies by Blind and Sighted Programmers', 2017, 'TSE',
                      'Armaly, A.; Rodeghero, P.; McMillan, C.',
                      [], 'Laboratory')
    e.median_task_duration = 1
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=1, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=23, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Wilcoxon')

    s = createSampling('Reward', e)
    addCharacteristic(newCharac='Industry experience', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=3, sample=s)
    addProfile(newProfile='Professionals', newQuantity=9, sample=s)


def createPaper30():
    e = newExperiment('The Scent of a Smell: An Extensive Comparison Between Textual and Structural Smells', 2017, 'TSE',
                      'Palomba, F.; Panichella, A.; Zaidman, A.; Oliveto, R.; De Lucia, A.',
                      [], 'Laboratory')
    e.median_task_duration = 2.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=4, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=12, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 1, 'Wilcoxon')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='programmin experience', sample=s)
    addCharacteristic(newCharac='Code Smells experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=19, sample=s)


# def createPaper31():
#     e = newExperiment('VT-Revolution: Interactive Programming Video Tutorial Authoring and Watching System', 2018, 'TSE',
#                       'Bao, L.; Xing, Z.; Xia, X.; Lo, D.',
#                       [], 'Laboratory')
#     e.median_task_duration = 2.5
#     #e.median_experiment_duration = 28
#     setExperimentDesign(newDesign='Factorial Design',
#                         explicity=0, treatmentQuantity=3, experiment=e)
#     addTask(newTaskType='COMPREENSION', newQuantity=12, experiment=e)

#     addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
#     addMeasuriment(experiment=e, newMeasure='TIME')

#     createStatistics(e, 1, 'Wilcoxon')

#     s = createSampling('Not Clear', e)
#     addCharacteristic(newCharac='programmin experience', sample=s)
#     addCharacteristic(newCharac='Code Smells experience', sample=s)

#     addProfile(newProfile='Professionals', newQuantity=19, sample=s)

def createPaper32():
    e = newExperiment('Cascade: A Universal Type Qualifier Inference Tool', 2015, 'ICSE',
                      'Vakilian, M.; Phaosawasdi, A.; Ernst, M. D.; Johnson, R. E.',
                      [], 'Laboratory')
    #e.median_task_duration = 2.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='within-subject, counterbalanced',
                        explicity=1, treatmentQuantity=4, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')

    createStatistics(e, 0, 'Welch t test')

    s = createSampling('Reward', e)
    addCharacteristic(newCharac='programming experience', sample=s)

    addProfile(newProfile='GradStudent', newQuantity=12, sample=s)


def createPaper34():
    e = newExperiment('A Longitudinal Cohort Study on the Retainment of Test-Driven Development', 2018, 'ESEM',
                      'Fucci, D.; Romano, S.; Baldassarre, M. T.; Caivano, D.; Scanniello, G.; Turhan, B.; Juristo, N.',
                      [], 'Laboratory')
    #e.median_task_duration = 2.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='repository')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 1, 'Shapiro-Wilk Test; Linear Mixed Model Analysis')

    s = createSampling('Extra Grade', e)
    addProfile(newProfile='Undergradstudent', newQuantity=30, sample=s)


def createPaper35():
    e = newExperiment('Syntax, predicates, idioms — what really affects code complexity?', 2019, 'ESE',
                      'Ajami, S.; Woodbridge, Y.; Feitelson, D. G.',
                      [], 'Home')
    #e.median_task_duration = 2.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Within Subject Design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=11, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='tool')

    createStatistics(
        e, 1, 't-test; Wilcoxon signed rank test, Welch t-test; correlation coefficient')

    s = createSampling('Reward', e)
    addCharacteristic(newCharac='gender', sample=s)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='programming experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=220, sample=s)


def createPaper36():
    e = newExperiment('Are Forward Designed or Reverse-Engineered UML Diagrams More Helpful for Code Maintenance?: A Controlled Experiment', 2013, 'EASE',
                      'Fernández-Sáez, A. M.; Chaudron, M. R.; Genero, M.; Ramos, I. ',
                      ['Wohlin et al.', 'Juristo and Moreno', 'Jedlitschka et al.'], 'Laboratory')
    e.median_task_duration = 2
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='between-subjects balanced design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=5, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(
        e, 0, 'Kolmogorov-Smirnov test; Levene test; Mann-Whitney test; ANOVA; T-test')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='grade', sample=s)
    addCharacteristic(newCharac='Professional experience', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=40, sample=s)


def createPaper37():
    e = newExperiment('Using Psycho-Physiological Measures to Assess Task Difficulty in Software Development', 2013, 'EASE',
                      'Fritz, T.; Begel, A.; Müller, S. C.; Yigit-Elliott, S.; Züger, M.',
                      [], 'Laboratory')
    e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=8, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')
    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='eye-tracking')
    addMeasuriment(experiment=e, newMeasure='Others', instrument='EDA')
    addMeasuriment(experiment=e, newMeasure='Others', instrument='EEG')

    createStatistics(
        e, 0, 'ANOVA')

    s = createSampling('Reward', e)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='gender', sample=s)
    addCharacteristic(newCharac='Professional experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=15, sample=s)


def createPaper39():
    e = newExperiment('A family of experiments to assess the effectiveness and efficiency of source code obfuscation techniques', 2014, 'ESEM',
                      'Ceccato, M.; Di Penta, M.; Falcarin, P.; Ricca, F.; Torchiano, M.; Tonella, P.',
                      ['Wohlin et al.'], 'Laboratory')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='counter-balanced design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='email')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='form')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='form')

    createStatistics(
        e, 1, 'Fishers exact test; x2 test; Mann-Whitney; ANOVA; repeated measures permutation test')

    s = createSampling('Not Clear', e)

    addProfile(newProfile='Gradstudent', newQuantity=61, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=13, sample=s)


def createPaper40():
    e = newExperiment('Understanding JavaScript Event-Based Interactions', 2014, 'ICSE',
                      'Alimadadi, S.; Sequeira, S.; Mesbah, A.; Pattabiraman, K.',
                      [], 'Laboratory')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 28
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='paper form')

    createStatistics(
        e, 0, 'Independent-samples t-tests with unequal variances')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Web programming experience', sample=s)
    addCharacteristic(newCharac='gender', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=14, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=2, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Company')
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e2)
    #e2.median_task_duration = 2
    addTask(newTaskType='COMPREENSION', newQuantity=4, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='TIME')
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE',
                   instrument='paper form')
    createStatistics(
        e2, 0, 'Independent-samples t-tests with unequal variances')

    s2 = createSampling('Not Clear', e2)
    addProfile(newProfile='Professionals', newQuantity=20, sample=s2)


def createPaper41():
    e = newExperiment('Comparing the Defect Reduction Benefits of Code Inspection and Test-Driven Development', 2011, 'TSE',
                      'Wilkerson, J. W.; Nunamaker, J. F.; Mercer, R.',
                      ['Wohlin et al.'], 'Home')
    #e.median_task_duration = 2
    e.median_experiment_duration = 14
    setExperimentDesign(newDesign='factorial design',
                        explicity=1, treatmentQuantity=4, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='form')

    createStatistics(
        e, 0, 't-test; Tests of normality; Levenes test; ANOVA')

    s = createSampling('Reward', e)

    addProfile(newProfile='Undergradstudent', newQuantity=29, sample=s)


def createPaper42():
    e = newExperiment('Descriptive Compound Identifier Names Improve Source Code Comprehension', 2018, 'ICSE',
                      'Schankin, A.; Berger, A.; Holt, D. V.; Hofmeister, J. C.; Riedel, T.; Beigl, M. ',
                      [], 'Home')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 14
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='DEGUGGING', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')

    createStatistics(
        e, 1, 'Cohens; t-test')

    s = createSampling('Not Clear', e)

    addProfile(newProfile='Student', newQuantity=50, sample=s)
    addProfile(newProfile='Professionals', newQuantity=38, sample=s)


def createPaper43():
    e = newExperiment('Drag-and-Drop Refactoring: Intuitive and Efficient Program Transformation', 2013, 'ICSE',
                      'Lee, Y. Y.; Chen, N.; Johnson, R. E.',
                      [], 'Home')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 14
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=9, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='screen recorder')

    createStatistics(
        e, 0, 'Wilcoxon')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Java experience', sample=s)
    addCharacteristic(newCharac='Eclipse experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=10, sample=s)


def createPaper45():
    e = newExperiment('Design of an Empirical Study for Comparing the Usability Concurrent Programming Languages', 2013, 'IST',
                      'Nanz, S.; Torshizi, F.; Pedroni, M.; Meyer, B.',
                      [], 'Laboratory')
    e.median_task_duration = 2
    #e.median_experiment_duration = 14
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)
    addTask(newTaskType='DEGUGGING', newQuantity=1, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='paper form')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='paper form')

    createStatistics(
        e, 0, 't-test')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='Java experience', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=67, sample=s)


def createPaper46():
    e = newExperiment('The Impact of Imperfect Change Rules on Framework API Evolution Identification: An Empirical Study', 2015, 'ESE',
                      'Wu, W.; Serveaux, A.; Guéhéneuc, Y. G.; Antoniol, G.',
                      [], 'Home')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 14
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=3, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=13, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='tool')

    createStatistics(
        e, 0, 't-test')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='gender', sample=s)
    addCharacteristic(newCharac='Professional experience', sample=s)
    addCharacteristic(newCharac='Java experience', sample=s)
    addCharacteristic(newCharac='Eclipse experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=22, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=9, sample=s)


def createPaper47():
    e = newExperiment('Evaluating Methods and Technologies in Software Engineering with Respect to Developers’ Skill Level', 2012, 'ICSE',
                      'Bergersen, G. R.; Sjøberg, D. I.',
                      [], 'Company')
    e.median_task_duration = 5
    e.median_experiment_duration = 2
    setExperimentDesign(newDesign='crossover design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=17, experiment=e)
    addTask(newTaskType='DEGUGGING', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE',
                   instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='tool')

    createStatistics(
        e, 1, 't-test; Spearman rho; Fisher test')

    s = createSampling('Voluntiers', e)
    #addCharacteristic(newCharac='gender', sample=s)

    addProfile(newProfile='Professionals', newQuantity=65, sample=s)


def createPaper48():
    e = newExperiment('Exploiting Dynamic Information in IDEs Improves Speed and Correctness of Software Maintenance Tasks', 2012, 'TSE',
                      'Rothlisberger, D.; Harry, M.; Binder, W.; Moret, P.; Ansaloni, D.; Villazon, A.; Nierstrasz, O.',
                      [], 'Company')
    e.median_task_duration = 2
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='DEGUGGING', newQuantity=1, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='form')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='Experimenter')

    createStatistics(
        e, 0, 'Kolmogorov-Smirnov; Levene test; t-test')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='Java Experience', sample=s)
    addCharacteristic(newCharac='Eclipse Experience', sample=s)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='scholar degree', sample=s)

    addProfile(newProfile='Professionals', newQuantity=30, sample=s)


def createPaper49():
    e = newExperiment('Supporting Selective Undo in a Code Editor', 2015, 'ICSE',
                      'Yoon, Y.; Myers, B. A.',
                      [], 'Laboratory')
    e.median_task_duration = 2
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='between-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(
        e, 0, 'Wilcoxon; t-test')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Student', newQuantity=12, sample=s)

def createPaper50():
    e = newExperiment('An External Replication on the Effects of Test-driven Development Using a Multi-site Blind Analysis Approach'
                      , 2015, 'ICSE',
                      'Fucci, D.; Scanniello, G.; Romano, S.; Shepperd, M.; Sigweni, B.; Uyaguari, F.; Oivo, M.',
                      [], 'Laboratory')
    e.median_task_duration = 3
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='Balanced crossover design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')

    createStatistics(
        e, 0, 'non-directional one-sample sign test;Kruskal-Wallis')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='Professional Experience', sample=s)
    addCharacteristic(newCharac='JUnit Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=12, sample=s)

def createPaper51():
    e = newExperiment('CodeHint: Dynamic and Interactive Synthesis of Code Snippets'
                      , 2014, 'ICSE',
                      'Galenson, J.; Reames, P.; Bodik, R.; Hartmann, B.; Sen, K.',
                      [], 'Laboratory')
    #e.median_task_duration = 3
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='within-subjects counterbalanced',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(
        e, 0, 't-test; qui-square test')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='Professional Experience', sample=s)s

    addProfile(newProfile='Student', newQuantity=12, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e2)
    e2.median_task_duration = 2
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='TIME')
    addMeasuriment(experiment=e2, newMeasure='CODE')
    createStatistics(
        e2, 0, 't-test; qui-square test')

    s2 = createSampling('Not Clear', e2)
    addProfile(newProfile='Gradstudent', newQuantity=2, sample=s2)
    addProfile(newProfile='Undergradstudent', newQuantity=12, sample=s2)

def createPaper52():
    e = newExperiment('Manual Refactoring Changes with Automated Refactoring Validation'
                      , 2014, 'ICSE',
                      'Ge, X.; Murphy-Hill, E.',
                      [], 'Laboratory')
    #e.median_task_duration = 3
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(
        e, 0, 'Mann-Whitney')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Student', newQuantity=6, sample=s)
    addProfile(newProfile='Professionals', newQuantity=2, sample=s)

def createPaper53():
    e = newExperiment('Does syntax highlighting help programming novices?'
                      , 2018, 'ESE',
                      'Hannebauer, C.; Hesenius, M.; Gruhn, V.',
                      [], 'Laboratory')
    e.median_task_duration = 1
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=20, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')

    createStatistics(
        e, 1, 'x2-statistic; Barnard’s Exact Test; Fisher’s Exact Test')

    s = createSampling('Part of Course', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Student', newQuantity=390, sample=s)

# def createPaper54(): # Removido

def createPaper55():
    e = newExperiment('Shorter identifier names take longer to comprehend'
                      , 2017, 'ICSE',
                      'Hofmeister, J.; Siegmund, J.; Holt, D. V.',
                      [], 'Laboratory')
    e.median_task_duration = 1
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='within-subjects balanced design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='DEGUGGING', newQuantity=20, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')

    createStatistics(e, 1, 'ANOVA')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='Industry Experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=72, sample=s)


def createPaper56():
    e = newExperiment('Revisit of Automatic Debugging via Human Focus-tracking Analysis'
                      , 2016, 'ICSE',
                      'Xie, X.; Liu, Z.; Song, S.; Chen, Z.; Xuan, J.; Xu, B.',
                      [], 'Laboratory')
    e.median_task_duration = 1.5
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='DEGUGGING', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE' , instrument = 'tool')
    addMeasuriment(experiment=e, newMeasure='TIME' , instrument = 'tool')

    createStatistics(e, 0, 't-test')

    s = createSampling('Part of Course', e)
    #addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Student', newQuantity=207, sample=s)

# def createPaper57(): Removido

def createPaper58():
    e = newExperiment('Feature Maintenance with Emergent Interfaces'
                      , 2014, 'ICSE',
                      'Ribeiro, M.; Borba, P.; Kästner, C.',
                      [], 'Laboratory')
    e.median_task_duration = 1.5
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='Latin Square design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE' , instrument = 'tool')
    addMeasuriment(experiment=e, newMeasure='TIME' , instrument = 'tool')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE' , instrument = 'screen recorder')

    createStatistics(e, 0, 'ANOVA; Bartlett; Box Cox; Tukey tests')

    s = createSampling('Voluntiers', e)
    #addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=10, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Company')
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e2)
    #e2.median_task_duration = 2
    addTask(newTaskType='COMPREENSION', newQuantity=4, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='CODE' , instrument = 'tool')
    addMeasuriment(experiment=e2, newMeasure='TIME' , instrument = 'tool')
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE' , instrument = 'screen recorder')
    createStatistics(
        e2, 0, 'ANOVA; Bartlett; Box Cox; Tukey tests')

    s2 = createSampling('Voluntiers', e2)
    addProfile(newProfile='Undergradstudent', newQuantity=14, sample=s2)


def createPaper59():
    e = newExperiment('Are Students Representatives of Professionals in Software Engineering Experiments?'
                      , 2014, 'ICSE',
                      'Salman, I.; Misirli, A. T.; Juristo, N.',
                      [], 'Laboratory')
    e.median_task_duration = 1.5
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='one-factor two-level, within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE' , instrument = 'tool')

    createStatistics(e, 0, 'Kolmogorov-Smirnov')

    s = createSampling('Part of Course', e)
    addCharacteristic(newCharac='nationality', sample=s)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=17, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='one-factor two-level, within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e2)
    #e2.median_task_duration = 2
    addTask(newTaskType='CONSTRUCTION', newQuantity=3, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='CODE' , instrument = 'tool')
    createStatistics(
        e2, 0, 'Kolmogorov-Smirnov')

    s2 = createSampling('Voluntiers', e2)
    addCharacteristic(newCharac='nationality', sample=s2)
    addCharacteristic(newCharac='Programming Experience', sample=s2)

    addProfile(newProfile='Professionals', newQuantity=24, sample=s2)


def createPaper60():
    e = newExperiment('Understanding Asynchronous Interactions in Full-Stack JavaScript'
                      , 2016, 'ICSE',
                      'Alimadadi, S.; Mesbah, A.; Pattabiraman, K.',
                      [], 'Laboratory')
    e.median_task_duration = 1.2
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=3, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME' , instrument = 'form')

    createStatistics(e, 0, 'MANOVA')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='gender', sample=s)
    addCharacteristic(newCharac='age', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=12, sample=s)

def createPaper61():
    e = newExperiment('Interactive Production Performance Feedback in the IDE'
                      , 2019, 'ICSE',
                      'Cito, J.; Leitner, P.; Rinard, M.; Gall, H. C. ',
                      [], 'Home')
    e.median_task_duration = 1.2
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME' , instrument = 'tool')

    createStatistics(e, 0, 'Shapiro-Wilk; Mann-Whitney')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=20, sample=s)

def createPaper62():
    e = newExperiment('Software Systems as Cities: A Controlled Experiment'
                      , 2011, 'ICSE',
                      'Wettel, R.; Lanza, M.; Robbes, R.',
                      [], 'Laboratory')
    e.median_task_duration = 1
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME' , instrument = 'tool')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE' , instrument = 'form')

    createStatistics(e, 0, 'ANOVA')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='gender', sample=s)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='nationality', sample=s)
    addCharacteristic(newCharac='Professional Experience', sample=s)
    addCharacteristic(newCharac='Java Experience', sample=s)
    addCharacteristic(newCharac='Eclipse Experience', sample=s)
    addCharacteristic(newCharac='Job Position', sample=s)

    addProfile(newProfile='Professionals', newQuantity=26, sample=s)

def createPaper63():
    e = newExperiment('Development of Auxiliary Functions: Should You Be Agile? An Empirical Assessment of Pair Programming and Test-First Programming'
                      , 2012, 'ICSE',
                      'Lemos, O. A. L.; Ferrari, F. C.; Silveira, F. F.; Garcia, A',
                      [], 'Laboratory')
    #e.median_task_duration = 1
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='repeated measures with cross-over experimental design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')
    addMeasuriment(experiment=e, newMeasure='Others' , details='test coverage')

    createStatistics(e, 0, 'Shapiro-Wilk; Wilcoxon/Mann-Whitney')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='gender', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=46, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='repeated measures with cross-over experimental design',
                        explicity=1, treatmentQuantity=2, experiment=e2)
    #e2.median_task_duration = 2
    addTask(newTaskType='CONSTRUCTION', newQuantity=6, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='TIME')
    addMeasuriment(experiment=e2, newMeasure='Others' , details='test coverage')
    createStatistics(
        e2, 0, 'Shapiro-Wilk; Wilcoxon/Mann-Whitney')

    s2 = createSampling('Not Clear', e2)

    addProfile(newProfile='Undergradstudent', newQuantity=39, sample=s2)

    # experiment 3
    e3 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='repeated measures with cross-over experimental design',
                        explicity=1, treatmentQuantity=2, experiment=e3)
    #e2.median_task_duration = 2
    addTask(newTaskType='CONSTRUCTION', newQuantity=6, experiment=e3)
    addMeasuriment(experiment=e3, newMeasure='TIME')
    addMeasuriment(experiment=e3, newMeasure='Others' , details='test coverage')
    createStatistics(
        e3, 0, 'Shapiro-Wilk; Wilcoxon/Mann-Whitney')

    s3 = createSampling('Not Clear', e3)
    addCharacteristic(newCharac='Professional Experience', sample=s3)
    addProfile(newProfile='Professionals', newQuantity=7, sample=s3)

def createPaper64():
    e = newExperiment('How Do API Documentation and Static Typing Affect API Usability?'
                      , 2014, 'ICSE',
                      'Endrikat, S.; Hanenberg, S.; Robbes, R.; Stefik, A.',
                      [], 'Laboratory')
    #e.median_task_duration = 1
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='factorial design',
                        explicity=1, treatmentQuantity=3, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')
    addMeasuriment(experiment=e, newMeasure='Others' , instrument = 'number of switches')

    createStatistics(e, 1, 'Shapiro–Wilk; T–Test; ANOVA; Levene Test')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='gender', sample=s)

    addProfile(newProfile='Student', newQuantity=25, sample=s)

def createPaper65():
    e = newExperiment('Overcoming Open Source Project Entry Barriers with a Portal for Newcomers'
                      , 2016, 'ICSE',
                      'Steinmacher, I.; Conte, T. U.; Treude, C.; Gerosa, M. A.',
                      [], 'Laboratory')
    e.median_task_duration = 5
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='factorial design',
                        explicity=1, treatmentQuantity=4, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form', details='TAM, self-estimation and diaries')

    createStatistics(e, 0, 'Wilcoxon; Cronbach’s Alpha reliability level')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='programming experience', sample=s)
    addCharacteristic(newCharac='programming laguages', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=14, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='factorial design',
                        explicity=1, treatmentQuantity=4, experiment=e2)
    #e2.median_task_duration = 2
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE', instrument='form', details='TAM, self-estimation and diaries')

    createStatistics(
        e2, 0, 'Wilcoxon; Cronbach’s Alpha reliability level')

    s2 = createSampling('Not Clear', e2)
    addCharacteristic(newCharac='programming experience', sample=s2)
    addCharacteristic(newCharac='programming laguages', sample=s2)
    addProfile(newProfile='Undergradstudent', newQuantity=51, sample=s2)

def createPaper66():
    e = newExperiment('Analyzing and Supporting Adaptation of Online Code Examples'
                      , 2019, 'ICSE',
                      'Zhang, T.; Yang, D.; Lopes, C.; Kim, M.',
                      [], 'Laboratory')
    e.median_task_duration = 0.5
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='between-subject design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')
    addMeasuriment(experiment=e, newMeasure='CODE')

    createStatistics(e, 1, 'Wilcoxon')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Java Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=14, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=2, sample=s)

def createPaper67():
    e = newExperiment('Test-Driven Code Review: An Empirical Study'
                      , 2019, 'ICSE',
                      'Zhang, T.; Yang, D.; Lopes, C.; Kim, M.',
                      [], 'Laboratory')
    e.median_task_duration = 0.5
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='partially counter-balanced repeated measures design',
                        explicity=1, treatmentQuantity=3, experiment=e)
    addTask(newTaskType='REVIEW', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='tool')

    createStatistics(e, 1, 'Remove outliers; Wilcoxon; ANOVA')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)
    addCharacteristic(newCharac='Java Experience', sample=s)
    addCharacteristic(newCharac='Review Experience', sample=s)
    addCharacteristic(newCharac='Hour Programming', sample=s)

    addProfile(newProfile='Professionals', newQuantity=62, sample=s)

def createPaper68():
    e = newExperiment('Improving Early Detection of Software Merge Conflicts'
                      , 2012, 'ICSE',
                      'Guimarães, M. L.; Silva, A. R.',
                      [], 'Laboratory')
    e.median_task_duration = 0.5
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='factorial design',
                        explicity=0, treatmentQuantity=3, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')
    addMeasuriment(experiment=e, newMeasure='Others', instrument='repository', details='resolve conflicts')

    createStatistics(e, 1, 'X2 test')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Eclipse Experience', sample=s)
    addCharacteristic(newCharac='Java Experience', sample=s)
    addCharacteristic(newCharac='Subversion Experience', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=21, sample=s)

def createPaper69():
    e = newExperiment('Initial findings on the evaluation of a model-based testing tool in the test design process'
                      , 2012, 'ICSE',
                      'Ferreira, L.; Nogueira, S.; Lima, L.; Fonseca, L.; Ferreira, W. ',
                      ['Wohlin et al.'], 'Laboratory')
    #e.median_task_duration = 0.5
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='one factor and two treatments with two blocking variables',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='TEST', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')

    createStatistics(e, 0, 'ANOVA; Pearson P test; Shapiro-Wilk normality test')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Test Experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=8, sample=s)

def createPaper70():
    e = newExperiment('Human and Program Factors Affecting the Maintenance of Programs with Deployed Design Patterns'
                      , 2012, 'IST',
                      'Ng, T. H.; Yu, Y. T.; Cheung, S. C.; Chan, W. K. ',
                      ['Wohlin et al.'], 'Laboratory')
    #e.median_task_duration = 0.5
    e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=3, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=3, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, '')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='Test Experience', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=55, sample=s)
    addProfile(newProfile='Gradstudent', newQuantity=63, sample=s)

def createPaper71():
    e = newExperiment('Bringing Test-Driven Development to Web Service Choreographies'
                      , 2015, 'JSS',
                      'Besson, F.; Moura, P.; Kon, F.; Milojicic, D.',
                      ['Kitchenham, B.', 'Seaman, C.B.'], 'Laboratory')
    #e.median_task_duration = 0.5
    e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 0, 'Kendall’s methodology')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=8, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='factorial design',
                        explicity=1, treatmentQuantity=4, experiment=e2)
    #e2.median_task_duration = 2
    addTask(newTaskType='CONSTRUCTION', newQuantity=4, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE', instrument='audio recorder')

    createStatistics(
        e2, 0, 'Kendall’s methodology')

    s2 = createSampling('Not Clear', e2)
    addCharacteristic(newCharac='Programming Experience', sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=8, sample=s2)
    addProfile(newProfile='Gradstudent', newQuantity=4, sample=s2)

def createPaper72():
    e = newExperiment('On the impact of trace-based feature location in the performance of software maintainers'
                      , 2013, 'JSS',
                      'de Almeida Maia, M.; Lafetá, R. F.',
                      ['Wohlin et al.'], 'Laboratory')
    e.median_task_duration = 4
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=3, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Kolmogorov-Smirnov; Shapiro-Wilk; Mann-Whitney test')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='Jog Description', sample=s)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=27, sample=s)

def createPaper73():
    e = newExperiment('Tempura: Temporal Dimension for IDEs'
                      , 2013, 'JSS',
                      'Lee, Y. Y.; Marinov, D.; Johnson, R. E.',
                      ['Juristo and Moreno'], 'Laboratory')
    e.median_task_duration = 1
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='between-group user study',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 't-test; Kolmogorov-Smirnov; Exact Bootstrap')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='Java Experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=1, sample=s)
    addProfile(newProfile='Gradstudent', newQuantity=9, sample=s)

def createPaper74(): #Parei aqui
    e = newExperiment('Labeling source code with information retrieval methods: an empirical study'
                      , 2014, 'ESE',
                      'De Lucia, A.; Di Penta, M.; Oliveto, R.; Panichella, A.; Panichella, S.',
                      [], 'Home')
    #e.median_task_duration = 1
    e.median_experiment_duration = 14
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=4, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=10, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 1, 'Wilcoxon; Holm’s correction procedure; Baker')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Java Experience', sample=s)
    addCharacteristic(newCharac='Professional Experience', sample=s)
    addCharacteristic(newCharac='Years programming', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=17, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Home')
    setExperimentDesign(newDesign='factorial design',
                        explicity=0, treatmentQuantity=4, experiment=e2)
    #e2.median_task_duration = 2
    e2.median_experiment_duration = 14
    addTask(newTaskType='COMPREENSION', newQuantity=10, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e2, newMeasure='TIME')

    createStatistics(
        e2, 1, 'Wilcoxon; Holm’s correction procedure; Baker')

    s2 = createSampling('Not Clear', e2)
    addCharacteristic(newCharac='Java Experience', sample=s2)
    addCharacteristic(newCharac='Professional Experience', sample=s2)
    addCharacteristic(newCharac='Years programming', sample=s2)

    addProfile(newProfile='Gradstudent', newQuantity=21, sample=s2)

def createPaper75():
    e = newExperiment('The impact of test-first programming on branch coverage and mutation score indicator of unit tests: An experiment'
                      , 2010, 'IST',
                      'Lee, Y. Y.; Marinov, D.; Johnson, R. E.',
                      [], 'Laboratory')
    #e.median_task_duration = 1
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', details= 'Test Coverage')

    createStatistics(e, 1, 'MANCOVA; Kolmogorov-Smirnov; Shapiro-Wilk; square root transformation, Levene’s test; Pillai’s trace; Wilk’s lambda; Hotelling’s trace; Roy’s largest root')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=22, sample=s)

def createPaper76():
    e = newExperiment('How Does the Degree of Variability Affect Bug Finding?'
                      , 2016, 'ICSE',
                      'Melo, J.; Brabrand, C.; Wąsowski, A.',
                      [], 'Laboratory')
    #e.median_task_duration = 1
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Latin Square',
                        explicity=1, treatmentQuantity=3, experiment=e)
    addTask(newTaskType='DEGUGGING', newQuantity=9, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')

    createStatistics(e, 0, 'Anova; Box Cox; Bartlett; Tukey')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)
    addCharacteristic(newCharac='Industry Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=69, sample=s)

def createPaper77():
    e = newExperiment('Empirical study on the maintainability of Web applications: Model-driven Engineering vs Code-centric'
                      , 2014, 'ESE',
                      'Martínez, Y.; Cachero, C.; Meliá, S.',
                      [], 'Laboratory')
    #e.median_task_duration = 1
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='two-way mixed model ANOVA design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=10, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='form')

    createStatistics(e, 0, 'ANOVA')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='gender', sample=s)
    addCharacteristic(newCharac='Programming Experience', sample=s)
    addCharacteristic(newCharac='age', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=27, sample=s)

def createPaper78():
    e = newExperiment('An Empirical Study on the Impact of C++ Lambdas and Programmer Experience'
                      , 2016, 'ICSE',
                      'Uesbeck, P. M., Stefik, A., Hanenberg, S., Pedersen, J., & Daleiden, P.',
                      [], 'Laboratory')
    e.median_task_duration = 0.45
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=10, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')

    createStatistics(e, 0, 'ANOVA')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='Academic Experimenter', sample=s)
    addCharacteristic(newCharac='Programming Experience', sample=s)
    addCharacteristic(newCharac='C++ Experience', sample=s)

    addProfile(newProfile='Student', newQuantity=42, sample=s)
    addProfile(newProfile='Professionals', newQuantity=12, sample=s)

def createPaper79():
    e = newExperiment('An Empirical Study on the Impact of C++ Lambdas and Programmer Experience'
                      , 2013, 'IST',
                      'Mäntylä, M. V.; Itkonen, J.',
                      [], 'Laboratory')
    #e.median_task_duration = 4
    e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='TEST', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'F-Score')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='credit', sample=s)
    addCharacteristic(newCharac='years of Study', sample=s)
    addCharacteristic(newCharac='Programming Experience', sample=s)
    addCharacteristic(newCharac='Test Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=130, sample=s)

def createPaper80():
    e = newExperiment('An Experimental Evaluation of Test Driven Development vs. Test-Last Development with Industry Professionals'
                      , 2014, 'EASE',
                      'Munir, H.; Wnuk, K.; Petersen, K.; Moayyed, M.',
                      [], 'Laboratory')
    #e.median_task_duration = 4
    e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='email')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='email')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 1, 'Shapiro-Wilk; Mann-Whitney; T-test')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='credit', sample=s)

    addProfile(newProfile='Professionals', newQuantity=31, sample=s)

def createPaper81():
    e = newExperiment('The impact of test case summaries on bug fixing performance: An empirical investigation'
                      , 2016, 'ICSE',
                      'Panichella, S.; Panichella, A.; Beller, M.; Zaidman, A.; Gall, H. C. ',
                      [], 'Laboratory')
    e.median_task_duration = 0.45
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='TEST', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', details='code and test')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='form')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 0, 'Shapiro-Wilk; Wilcoxon; two-way permutation test')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=12, sample=s)
    addProfile(newProfile='Gradstudent', newQuantity=19, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=2, sample=s)

def createPaper82():
    e = newExperiment('Links between the Personalities, Styles and Performance in Computer Programming'
                      , 2016, 'JSS',
                      'Karimi, Z.; Baraani-Dastjerdi, A.; Ghasem-Aghaee, N.; Wagner, S.',
                      [], 'Laboratory')
    e.median_task_duration = 0.45
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=6, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='repository')

    createStatistics(e, 0, 'Pearson correlation coefficient')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='personality', sample=s)
    addCharacteristic(newCharac='programming experience', sample=s)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='gender', sample=s)
    addCharacteristic(newCharac='year of study', sample=s)

    addProfile(newProfile='Student', newQuantity=65, sample=s)

def createPaper83():
    e = newExperiment('Do Developers Read Compiler Error Messages?'
                      , 2017, 'ICSE',
                      'Barik, T.; Smith, J.; Lubick, K.; Holmes, E.; Feng, J.; Murphy-Hill, E.; Parnin, C.',
                      [], 'Laboratory')
    e.median_task_duration = 1
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=6, experiment=e)
    addTask(newTaskType='DEGUGGING', newQuantity=10, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')
    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='eye traker')

    createStatistics(e, 0, 't-test; Chi-squared')

    s = createSampling('Extra Grade', e)
    #addCharacteristic(newCharac='Eclispe experience', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=56, sample=s)

def createPaper84():
    e = newExperiment('Prompter Turning the IDE into a self-confident programming assistant'
                      , 2016, 'ESE',
                      'Luca, P.; Gabriele, B.; Di Penta, M.; Rocco, O.; Michele, L.',
                      [], 'Laboratory')
    e.median_task_duration = 2
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='paired design one factor and two treatments',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 0, 'Wilcoxon; Mann-Whitney; Holm’s correction; ANOVA')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming experience', sample=s)
    addCharacteristic(newCharac='Java experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=3, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=3, sample=s)
    addProfile(newProfile='Professionals', newQuantity=6, sample=s)

def createPaper85():
    e = newExperiment('Supporting Software Developers with a Holistic Recommender System'
                      , 2017, 'ICSE',
                      'Ponzanelli, L.; Scalabrino, S.; Bavota, G.; Mocci, A.; Oliveto, R.; Di Penta, M.; Lanza, M.',
                      [], 'Laboratory')
    e.median_task_duration = 1.6
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 1, 'Shapiro-Wilk; Wilcoxon; ANOVA')

    s = createSampling('Part of Course', e)
    addCharacteristic(newCharac='Programming experience', sample=s)
    addCharacteristic(newCharac='Java experience', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=16, sample=s)

def createPaper86():
    e = newExperiment('Portfolio: Finding Relevant Functions and Their Usages'
                      , 2011, 'ICSE',
                      'McMillan, C.; Grechanik, M.; Poshyvanyk, D.; Xie, Q.; Fu, C.',
                      [], 'Laboratory')
    e.median_task_duration = 2
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='cross validation experimental design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='COMPREENSION', newQuantity=5, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 0, 'ANOVA; t-tests; x2')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming experience', sample=s)
    addCharacteristic(newCharac='C++ experience', sample=s)
    addCharacteristic(newCharac='Koders experience', sample=s)
    addCharacteristic(newCharac='Google Search experience', sample=s)

    addProfile(newProfile='GradStudent', newQuantity=5, sample=s)
    addProfile(newProfile='Professionals', newQuantity=44, sample=s)

def createPaper87():
    e = newExperiment('An empirical study on the impact of AspectJ on software evolvability'
                      , 2011, 'ICSE',
                      'McMillan, C.; Grechanik, M.; Poshyvanyk, D.; Xie, Q.; Fu, C.',
                      [], 'Laboratory')
    e.median_task_duration = 2
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Shapiro–Wilk; F-test; T-test; Mann-Whitney')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='Java experience', sample=s)

    addProfile(newProfile='Student', newQuantity=35, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e2)
    e2.median_task_duration = 2
    #e2.median_experiment_duration = 14
    addTask(newTaskType='CONSTRUCTION', newQuantity=10, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e2, newMeasure='TIME')

    createStatistics(
        e2, 1, 'Fisher; Mann-Whitney')

    s2 = createSampling('Voluntiers', e2)
    addCharacteristic(newCharac='Java Experience', sample=s2)

    addProfile(newProfile='Gradstudent', newQuantity=24, sample=s2)

def createPaper88():
    e = newExperiment('Noise in Mylyn interaction traces and its impact on developers and recommendation systems'
                      , 2018, 'ESE',
                      'Soh, Z.; Khomh, F.; Guéhéneuc, Y. G.; Antoniol, G.',
                      ['Wohlin et al.'], 'Home')
    #e.median_task_duration = 0.8
    #e.median_experiment_duration = 30
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='REVIEW', newQuantity=3, experiment=e)

    addMeasuriment(experiment=e, newMeasure='Others', details='MRI scanner data')

    createStatistics(e, 1, 'Wilcoxon')

    s = createSampling('Reward', e)
    addCharacteristic(newCharac='Java experience', sample=s)

    addProfile(newProfile='GradStudent', newQuantity=2, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=27, sample=s)

def createPaper89():
    e = newExperiment('Plat_Forms 2011: Finding Emergent Properties of Web Application Development Platforms'
                      , 2018, 'ESE',
                      'Soh, Z.; Khomh, F.; Guéhéneuc, Y. G.; Antoniol, G.',
                      [], 'Laboratory')
    #e.median_task_duration = 0.8
    e.median_experiment_duration = 2
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=5, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='USB stick')

    createStatistics(e, 0, '')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Professional experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=16, sample=s)

def createPaper90():
    e = newExperiment('Structural Complexity and Programmer Team Strategy: An Experimental Test'
                      , 2011, 'TSE',
                      'Ramasubbu, N.; Kemerer, C. F.; Hong, J.',
                      [], 'Laboratory')
    e.median_task_duration = 2
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='between-subjects experiment design',
                        explicity=1, treatmentQuantity=2, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='repository')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='screen recorder')

    createStatistics(e, 1, 'Shapiro-Wilk; ANOVA; MANOVA; Bonferroni adjustment')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='Professional experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=90, sample=s)

def createPaper91():
    e = newExperiment('Decoding the representation of code in the brain: An fMRI study of code review and expertise'
                      , 2011, 'TSE',
                      'Floyd, B.; Santander, T.; Weimer, W.',
                      [], 'Laboratory')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 2
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=3, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='repository')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='screen recorder')

    createStatistics(e, 1, 'Shapiro-Wilk; ANOVA; MANOVA; Bonferroni adjustment')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='Professional experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=90, sample=s)

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
    createPaper12()
    createPaper13()
    createPaper14()
    createPaper15()
    createPaper16()
    createPaper17()
    createPaper18()
    createPaper19()
    createPaper20()
    createPaper21()
    createPaper22()
    createPaper23()
    createPaper24()
    createPaper25()
    createPaper26()
    createPaper27()
    createPaper28()
    createPaper29()
    createPaper30()
    createPaper32()
    createPaper34()
    createPaper36()
    createPaper37()
    createPaper39()
    createPaper40()
    createPaper41()
    createPaper42()
    createPaper43()
    createPaper45()
    createPaper46()
    createPaper47()
    createPaper48()
    createPaper49()
    createPaper50()
    createPaper51()
    createPaper52()
    createPaper53()
    createPaper55()
    createPaper56()
    createPaper58()
    createPaper59()
    createPaper60()
    createPaper61()
    createPaper62()
    createPaper63()
    createPaper64()
    createPaper65()
    createPaper66()
    createPaper67()
    createPaper68()
    createPaper69()
    createPaper70()
    createPaper71()
    createPaper72()
    createPaper73()
    createPaper75()
    createPaper76()
    createPaper78()
    createPaper79()
    createPaper80()
    createPaper81()
    createPaper82()
    createPaper83()
    createPaper85()
    createPaper86()
    createPaper88()
    createPaper89()
    createPaper90()
    createPaper91()

    db.session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

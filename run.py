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
    createAGuideline('A practical guide for using statistical tests to assess randomized algorithms in software engineering',
                     'A. Arcuri, L. Briand')
    createAGuideline('A critique and improvement of the cl common language effect size statistics of mcgraw and wong',
                     'A. Vargha , H.D. Delaney')

    for g in guides.values():
        db.session.add(g)
    db.session.commit()


def createAGuideline(newTitle, newAuthors):
    g = Guideline(title=newTitle.lower(), authors=newAuthors.lower())
    guides[newAuthors] = g


def newExperiment(newTitle, newYear, newVenue, newAuthors, guidelines, newSettings):
    p = Publication(title=newTitle, year=newYear, venue=newVenue.lower(),
                    authors=newAuthors.lower())
    e = Experiment(settings=newSettings.lower())
    for g in guidelines:
        p.guidelines.append(guides[g])
    p.experiments.append(e)
    db.session.add(p)
    db.session.add(e)
    return e


def addExperiment(experiment, newSettings):
    e = Experiment(settings=newSettings.lower())
    experiment.exp_pub.experiments.append(e)

    db.session.add(e)
    return e

def addTask(newTaskType, newQuantity, experiment):
    t = Task(task_type=newTaskType.lower(), quantity=newQuantity)
    t.task_parent = experiment
    db.session.add(t)


def setExperimentDesign(newDesign, explicity, treatmentQuantity, experiment, normalizedDesing):
    d = ExperimentDesign(design_description=newDesign.lower(), is_explicity_design=explicity,
                         treatment_quantity=treatmentQuantity, design_normalized=normalizedDesing)
    experiment.design = d
    db.session.add(d)


def createSampling(strategy, experiment):
    s = Sampling()
    s.exp = experiment
    r = Recruting(recruiting_strategy=strategy.lower(), parent_recru=s)
    db.session.add(s)
    db.session.add(r)
    return s


def addProfile(newProfile, newQuantity, sample):
    sp = SamplingProfile(profile=newProfile.lower(),
                         quantity=newQuantity, parent_profile=sample)
    db.session.add(sp)


def addCharacteristic(newCharac, sample):
    sc = SamplingCharacteristic(charac=newCharac.lower(), parent_charac=sample)
    db.session.add(sc)


def addMeasuriment(experiment, newMeasure='TIME', instrument=None, details=None):
    m = Measurement(measurement_type=newMeasure.lower())
    if (instrument):
        m.measurement_instruments = instrument.lower()
    if (details):
        m.measurement_details = details.lower()
    experiment.measurements.append(m)
    db.session.add(m)

# def attachDesign(experiment, ReclassifiedDesing):
#     experiment.design_normalized=ReclassifiedDesing
#     print('ReclassifiedDesing='+ReclassifiedDesing)

def createStatistics(experiment, hasPower=0, details=None, np_p=0):
    s = Statistics(has_power=hasPower, statistic_details=details.lower())
    s.p_or_np = np_p
    s.exp = experiment
    db.session.add(s)


def createPaper1():
    e = newExperiment('Answering software evolution questions: An empirical evaluation', 2013, 'IST',
                      'Lile Hattori; Marco D’Ambros; Michele Lanza; Mircea Lungu',
                      ['Wohlin et al.'], 'Laboratory')
    # attachDesign(e, 'Independent groups')
    e.median_experiment_duration = 0.5
    addTask(newTaskType='COMPREHENSION', newQuantity=6, experiment=e)
    setExperimentDesign(newDesign='between-subjects with balanced design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    s = createSampling('Voluntiers', e)
    addProfile(newProfile='GradStudent', newQuantity=44, sample=s)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='sex', sample=s)
    addCharacteristic(newCharac='nationality', sample=s)
    addCharacteristic(newCharac='Level of experience', sample=s)
    addCharacteristic(newCharac='Years of experience', sample=s)
    addCharacteristic(newCharac='Linux experience', sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='paper form')
    createStatistics(e, 0, 'Shapiro-Wilk test; Student’s t-test; Mann-Whitney test', 2)


def createPaper2():
    e = newExperiment('The impact of Software Testing education on code reliability: An empirical assessment', 2018, 'JSS',
                      'Otávio Augusto Lazzarini Lemos; Fábio Fagundes Silveira; Fabiano Cutigi Ferrari; Alessandro Garcia',
                      ['Montgomery et al.'], 'Laboratory')
    # attachDesign(e, 'Pretest and posttest control')
    e.median_task_duration = 2

    addTask(newTaskType='CONSTRUCTION', newQuantity=4, experiment=e)
    setExperimentDesign(newDesign='pre-post test with control group',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Pretest and posttest control')
    s = createSampling('Not Clear', e)
    addProfile(newProfile='GradStudent', newQuantity=60, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='paper form')
    createStatistics(e, 0, 'Student’s t-test; Shapiro-Wilk test', 2)


def createPaper3():
    e = newExperiment('A replicated experiment for evaluating the effectiveness of pairing practice in PSP education', 2019, 'JSS',
                      'Guoping Rong; He Zhang; Bohan Liu; Qi Shan; Dong Shao',
                      [], 'Laboratory')
    # attachDesign(e, 'Independent groups')
    e.median_task_duration = 2
    addTask(newTaskType='CONSTRUCTION', newQuantity=4, experiment=e)
    setExperimentDesign(newDesign='Not Clear',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    s = createSampling('Not Clear', e)
    addProfile(newProfile='GradStudent', newQuantity=120, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='Experimenter and log')
    addMeasuriment(experiment=e, newMeasure='Others',
                   details='Number Of Errors')
    addMeasuriment(experiment=e, newMeasure='Others', details='grade')
    createStatistics(e, 0, 'Wilcoxon Signed Rank Test')


def createPaper4():
    e = newExperiment('On some end-user programming constructs and their understandability', 2018, 'JSS',
                      'M Mackowiak,; J Nawrocki; M Ochodek',
                      [], 'Laboratory')
    # attachDesign(e, 'Independent groups')
    e.median_experiment_duration = 0.1
    addTask(newTaskType='COMPREHENSION', newQuantity=1, experiment=e)
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=1, treatmentQuantity=1, experiment=e, normalizedDesing='Independent groups')
    s = createSampling('Not Clear', e)
    addProfile(newProfile='Undergradstudent', newQuantity=114, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')
    createStatistics(e, 1, 'Mann-Whitney test; Wilcoxon Signed Rank Test; Shapiro-Wilk test; Fisher`s exact test; Cliff’s δ effect')


def createPaper5():
    e = newExperiment('A controlled experiment in assessing and estimating software maintenance tasks', 2018, 'JSS',
                      'M Mackowiak,; J Nawrocki; M Ochodek',
                      [], 'Laboratory')
    # attachDesign(e, 'Independent groups')
    e.median_experiment_duration = 7
    addTask(newTaskType='MAINTENANCE', newQuantity=6, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=6, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=5, experiment=e)
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=3, experiment=e, normalizedDesing='Independent groups')
    s = createSampling('Not Clear', e)
    addProfile(newProfile='Undergradstudent', newQuantity=23, sample=s)
    addProfile(newProfile='GradStudent', newQuantity=1, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='paper form')
    createStatistics(e, 0, 'Kruskal-Wallis test; Mann-Whitney test')


def createPaper6():
    e = newExperiment('Impact of test-driven development on productivity, code and tests: A controlled experiment', 2011, 'IST',
                      'M Pancur; M Ciglaric',
                      ['Wohlin et al.', 'Lott and Rombach'], 'Laboratory and Home')
    e.median_experiment_duration = 35
    e.median_task_duration = 4
    # attachDesign(e, '4-group crossover')
    addTask(newTaskType='CONSTRUCTION', newQuantity=9, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=9, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=9, experiment=e)
    setExperimentDesign(newDesign='standard one factor and two treatments',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='4-group crossover')
    s = createSampling('Voluntiers', e)
    addProfile(newProfile='GradStudent', newQuantity=34, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE', instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')
    addCharacteristic(newCharac='Java experience', sample=s)
    addCharacteristic(newCharac='Programming experience', sample=s)
    addCharacteristic(newCharac='OO experience', sample=s)
    addCharacteristic(newCharac='Industry experience', sample=s)
    createStatistics(e, 1, 'Kolmogorov-Smirnov test; Shapiro-Wilk test; Mann-Whitney test; Pearson P test; Cohen’s d; Wilcoxon Signed Rank Test')


def createPaper7():
    e = newExperiment('Evaluating the productivity of a reference-based programming approach: A controlled experiment', 2014, 'IST',
                      'A Sturm; O Kramer',
                      [], 'Laboratory')
    e.median_experiment_duration = 0.1
    e.median_task_duration = 9
    # attachDesign(e, 'Independent groups')
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)
    setExperimentDesign(newDesign='standard one factor and two treatments',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    s = createSampling('Voluntiers', e)
    addProfile(newProfile='GradStudent', newQuantity=50, sample=s)
    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='paper form')
    createStatistics(e, 0, 'Mann-Whitney test')


def createPaper9():
    e = newExperiment('Towards an operationalization of test-driven development skills: An industrial empirical study', 2015, 'IST',
                      'Fucci, D.; Turhan, B.; Juristo, N.; Dieste, O.; Tosun-Misirli, A.; Oivo, M.',
                      [], 'Company')
    e.median_experiment_duration = 5
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=1, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='CONSTRUCTION', newQuantity=3, experiment=e)
    addMeasuriment(experiment=e, newMeasure='CODE')
    createStatistics(e, 1, 'ANOVA; Bartlett’s test')

    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Professionals', newQuantity=30, sample=s)


def createPaper10():
    e = newExperiment('Tester interactivity makes a difference in search-based software testing: A controlled experiment', 2016, 'IST',
                      'Marculescu, B.; Poulding, S.; Feldt, R.; Petersen, K.; Torkar, R. ',
                      ['A. Arcuri, L. Briand', 'A. Vargha , H.D. Delaney'], 'Company')
    e.median_task_duration = 0.75
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='crossover design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='TEST', newQuantity=1, experiment=e)
    addTask(newTaskType='TEST', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='form')
    addMeasuriment(experiment=e, newMeasure='CODE', details='test cases')
    createStatistics(e, 1, 'Mann-Whitney test; Vargha and Delaney')

    s = createSampling('part of Course', e)
    addProfile(newProfile='Gradstudent', newQuantity=58, sample=s)


def createPaper12():
    e = newExperiment('Live programming in practice: A controlled experiment on state machines for robotic behaviors', 2018, 'IST',
                      'Campusano, M.; Fabry, J.; Bergel, A.',
                      [], 'Laboratory')
    # attachDesign(e, '4-group crossover')
    # experiment 1
    e.median_task_duration = 4
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='4-group crossover')
    addTask(newTaskType='COMPREHENSION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')
    createStatistics(e, 0, 'Mann-Whitney test')

    s = createSampling('Not Clear', e)
    addProfile(newProfile='Gradstudent', newQuantity=2, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=8, sample=s)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='Scholarity', sample=s)
    addCharacteristic(newCharac='tool expertize', sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e2, normalizedDesing='4-group crossover')
    # attachDesign(e2, '4-group crossover')
    addTask(newTaskType='CONSTRUCTION', newQuantity=3, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e2, newMeasure='TIME')
    createStatistics(e2, 0, 'Mann-Whitney test')

    s2 = createSampling('Not Clear', e2)
    addProfile(newProfile='Gradstudent', newQuantity=2, sample=s2)
    addProfile(newProfile='Undergradstudent', newQuantity=8, sample=s2)


def createPaper14():
    e = newExperiment('The impact of test-first programming on branch coverage and mutation score indicator of unit tests: An experiment', 2010, 'IST',
                      'Madeyski L.',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 5
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='design is one factor with the two treatments',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='CONSTRUCTION;TEST', newQuantity=10, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='repository')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='paper form')

    createStatistics(
        e, 1, 'Kolmogorov-Smirnov test; Shapiro-Wilk test; Mahalanobis distance;' +
        ' Levene test; Test of Equality of Covariance Matrices; MANCOVA')

    s = createSampling('Part of Course', e)
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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='counterbalanced within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='upload')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='form')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 0, 'MANOVA; Wilcoxon Signed Rank Test')

    s = createSampling('Not Clear', e)
    addProfile(newProfile='GradStudent', newQuantity=13, sample=s)


def createPaper16():
    e = newExperiment('An Empirical Study on the Developers’ Perception of Software Coupling', 2013, 'ICSE',
                      'Bavota, G.; Dit, B.; Oliveto, R.; Di Penta, M.; Poshyvanyk, D.; De Lucia, A.',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=4, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='COMPREHENSION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')

    createStatistics(e, 1, 'Mann-Whitney test; Cliff’s δ effect')

    s = createSampling('Voluntiers', e)
    addProfile(newProfile='GradStudent', newQuantity=49, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=10, sample=s)
    addProfile(newProfile='Professionals', newQuantity=14, sample=s)


def createPaper17():
    e = newExperiment('Recommending Source Code for Use in Rapid Software Prototypes', 2012, 'ICSE',
                      'McMillan, C.; Hariri, N.; Poshyvanyk, D.; Cleland-Huang, J.; Mobasher, B.',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='Cross-Validation Design',
                        explicity=1, treatmentQuantity=4, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='CONSTRUCTION', newQuantity=6, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=6, experiment=e)

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='COMPREHENSION', newQuantity=4, experiment=e)

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
                      ['Juristo and Moreno', 'Wohlin et al.', 'Jedlitschka et al.'], 'Laboratory')
    e.median_task_duration = 0.5
    e.median_experiment_duration = 0.1
    # attachDesign(e, 'crossover design')
    # setExperimentDesign(newDesign='ABBA crossover design', explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    setExperimentDesign(newDesign='AB/BA crossover design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='COMPREHENSION', newQuantity=1, experiment=e)
    addTask(newTaskType='COMPREHENSION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')

    createStatistics(e, 1, 'Mann-Whitney test; Shapiro-Wilk test; Cliff’s δ effect')

    s = createSampling('Extra Grade', e)
    addProfile(newProfile='Undergradstudent', newQuantity=55, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    # attachDesign(e2, 'crossover design')
    setExperimentDesign(newDesign='AB/BA crossover design',
                        explicity=1, treatmentQuantity=2, experiment=e2, normalizedDesing='crossover design')
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e2)
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='CODE')
    createStatistics(e2, 1, 'Mann-Whitney test; Shapiro-Wilk test')

    s2 = createSampling('Extra Grade', e2)
    addProfile(newProfile='Undergradstudent', newQuantity=42, sample=s2)


def createPaper20():
    e = newExperiment('Developer Reading Behavior While Summarizing Java Methods: Size and Context Matters', 2019, 'ICSE',
                      'Abid, N. J.; Sharif, B.; Dragan, N.; Alrasheed, H.; Maletic, J. I. ',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=1, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='COMPREHENSION', newQuantity=23, experiment=e)

    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='eye traker')
    addMeasuriment(experiment=e, newMeasure='CODE',
                   instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='tool')

    createStatistics(e, 1, 'Wilcoxon Signed Rank Test; Bonferroni p-value correction; Cohen’s d')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='between-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='DEGUGGING', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Mann-Whitney test')

    s = createSampling('Not Clear', e)
    addProfile(newProfile='Undergradstudent', newQuantity=18, sample=s)


def createPaper22():
    e = newExperiment('The Effect of Poor Source Code Lexicon and Readability on Developers’ Cognitive Load', 2018, 'ICSE',
                      'Fakhoury, S.; Ma, Y.; Arnaoudova, V.; Adesope, O. ',
                      [], 'Laboratory')
    #e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=4, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='DEGUGGING', newQuantity=1, experiment=e)
    addTask(newTaskType='COMPREHENSION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='eye traker')
    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='Brain Image')

    createStatistics(e, 1, 'Wilcoxon Signed Rank Test; Cliff’s δ effect')

    s = createSampling('Reward', e)
    addProfile(newProfile='Professionals', newQuantity=15, sample=s)


def createPaper23():
    e = newExperiment('A Controlled Experiment for Program Comprehension through Trace Visualization', 2018, 'ICSE',
                      'Cornelissen, B.; Zaidman, A.; van Deursen, A.',
                      [], 'Laboratory')
    e.median_task_duration = 1.5
    #e.median_experiment_duration = 28
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='COMPREHENSION', newQuantity=8, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='form')
    addMeasuriment(experiment=e, newMeasure='CODE')

    createStatistics(e, 0, 'Kolmogorov-Smirnov test; Levene test; Student’s t-test')

    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Gradstudent', newQuantity=26, sample=s)
    addProfile(newProfile='Professionals', newQuantity=8, sample=s)


def createPaper24():
    e = newExperiment('A Controlled Experiment for Evaluating the Impact of Coupling on the Maintainability of Service-Oriented Software', 2010, 'TSE',
                      'Cornelissen, B.; Zaidman, A.; van Deursen, A.',
                      ['R. Moen, T. Nolan, and L. Provost'], 'Laboratory')
    e.median_task_duration = 3
    #e.median_experiment_duration = 28
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='incomplete within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='Experimenter')

    createStatistics(
        e, 1, 'Shapiro-Wilk test; G*Power 3; ANOVA')

    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Gradstudent', newQuantity=5, sample=s)


def createPaper25():
    e = newExperiment('Improving Source Code Lexicon via Traceability and Information Retrieval', 2010, 'TSE',
                      'De Lucia, A.; Di Penta, M.; Oliveto, R.',
                      [], 'Laboratory')
    e.median_task_duration = 2
    e.median_experiment_duration = 0.1
    # attachDesign(e, '4-group crossover')
    setExperimentDesign(newDesign='completely balanced design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='4-group crossover')
    addTask(newTaskType='MAINTENANCE', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='form')

    createStatistics(e, 1, 'Shapiro-Wilk test; Mann-Whitney test')

    s = createSampling('Voluntiers', e)
    addProfile(newProfile='Gradstudent', newQuantity=16, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    # attachDesign(e2, '4-group crossover')
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e2, normalizedDesing='4-group crossover')
    e2.median_task_duration = 2
    addTask(newTaskType='MAINTENANCE', newQuantity=2, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='CODE')
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE',
                   instrument='form')
    createStatistics(e2, 1, 'Mann-Whitney test; Shapiro-Wilk test; ANOVA')

    s2 = createSampling('Extra Grade', e2)
    addProfile(newProfile='Undergradstudent', newQuantity=20, sample=s2)


def createPaper26():
    e = newExperiment('Preserving Aspects via Automation: a Maintainability Study', 2011, 'ESEM',
                      'Hovsepyan, A., Scandariato, R., Van Baelen, S., Joosen, W., & Demeyer, S.',
                      [], 'Laboratory')
    e.median_task_duration = 3
    #e.median_experiment_duration = 28
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 1, 'Lilliefors test; Mann-Whitney test; ANCOVA')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='INSPECTION', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Chi-squared Tests')

    s = createSampling('Voluntiers', e)

    addProfile(newProfile='Professionals', newQuantity=15, sample=s)


def createPaper29():
    e = newExperiment('A Comparison of Program Comprehension Strategies by Blind and Sighted Programmers', 2017, 'TSE',
                      'Armaly, A.; Rodeghero, P.; McMillan, C.',
                      [], 'Laboratory')
    e.median_task_duration = 1
    #e.median_experiment_duration = 28
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='COMPREHENSION', newQuantity=23, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Mann-Whitney test')

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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=3, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 1, 'Wilcoxon Signed Rank Test')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Industry experience', sample=s)
    addCharacteristic(newCharac='programming experience', sample=s)
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
#     addTask(newTaskType='COMPREHENSION', newQuantity=12, experiment=e)

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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='within-subject, counterbalanced',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)

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
    # attachDesign(e, '4-group crossover')
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='4-group crossover')
    addTask(newTaskType='CONSTRUCTION', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='repository')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 1, 'Shapiro-Wilk test; Linear Mixed Model Analysis')

    s = createSampling('Extra Grade', e)
    addProfile(newProfile='Undergradstudent', newQuantity=30, sample=s)


def createPaper35():
    e = newExperiment('Syntax, predicates, idioms — what really affects code complexity?', 2019, 'ESE',
                      'Ajami, S.; Woodbridge, Y.; Feitelson, D. G.',
                      [], 'Home')
    #e.median_task_duration = 2.5
    #e.median_experiment_duration = 28
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='Within Subject Design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='COMPREHENSION', newQuantity=6, experiment=e)
    addTask(newTaskType='COMPREHENSION', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='tool')

    createStatistics(
        e, 1, 't-test; Wilcoxon Signed Rank Test; Welch t-test; correlation coefficient')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='between-subjects balanced design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=5, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(
        e, 0, 'Kolmogorov-Smirnov test; Levene test; Mann-Whitney test; ANOVA; T-test')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='grade', sample=s)
    addCharacteristic(newCharac='Professional experience', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=40, sample=s)


# def createPaper37():
#     e = newExperiment('Using Psycho-Physiological Measures to Assess Task Difficulty in Software Development', 2013, 'ICSE',
#                       'Fritz, T.; Begel, A.; Müller, S. C.; Yigit-Elliott, S.; Züger, M.',
#                       [], 'Laboratory')
#     e.median_task_duration = 1.5
#     #e.median_experiment_duration = 28
#     setExperimentDesign(newDesign='',
#                         explicity=0, treatmentQuantity=2, experiment=e)
#     addTask(newTaskType='COMPREHENSION', newQuantity=8, experiment=e)

#     addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')
#     addMeasuriment(experiment=e, newMeasure='Others',
#                    instrument='eye-tracking')
#     addMeasuriment(experiment=e, newMeasure='Others', instrument='EDA')
#     addMeasuriment(experiment=e, newMeasure='Others', instrument='EEG')

#     createStatistics(
#         e, 0, 'ANOVA')

#     s = createSampling('Reward', e)
#     addCharacteristic(newCharac='age', sample=s)
#     addCharacteristic(newCharac='gender', sample=s)
#     addCharacteristic(newCharac='Professional experience', sample=s)

#     addProfile(newProfile='Professionals', newQuantity=15, sample=s)


def createPaper39():
    e = newExperiment('A family of experiments to assess the effectiveness and efficiency of source code obfuscation techniques', 2014, 'ESEM',
                      'Ceccato, M.; Di Penta, M.; Falcarin, P.; Ricca, F.; Torchiano, M.; Tonella, P.',
                      ['Wohlin et al.'], 'Laboratory')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 28
    # attachDesign(e, '4-group crossover')
    setExperimentDesign(newDesign='counter-balanced design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='4-group crossover')
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='email')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='form')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='form')

    createStatistics(
        e, 1, 'Fisher`s exact test; x2 test; Mann-Whitney test; ANOVA; repeated measures permutation test')

    s = createSampling('Not Clear', e)

    addProfile(newProfile='Gradstudent', newQuantity=61, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=13, sample=s)


def createPaper40():
    e = newExperiment('Understanding JavaScript Event-Based Interactions', 2014, 'ICSE',
                      'Alimadadi, S.; Sequeira, S.; Mesbah, A.; Pattabiraman, K.',
                      ['Wohlin et al.'], 'Laboratory')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 28
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='COMPREHENSION', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='paper form')

    createStatistics(
        e, 0, 't-test; Mann-Whitney test')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Web programming experience', sample=s)
    addCharacteristic(newCharac='gender', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=14, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=2, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Company')
    # attachDesign(e2, 'Independent groups')
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e2, normalizedDesing='Independent groups')
    #e2.median_task_duration = 2
    addTask(newTaskType='COMPREHENSION', newQuantity=4, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='TIME')
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE',
                   instrument='paper form')
    createStatistics(
        e2, 0, 't-test')

    s2 = createSampling('Not Clear', e2)
    addProfile(newProfile='Professionals', newQuantity=20, sample=s2)


def createPaper41():
    e = newExperiment('Comparing the Defect Reduction Benefits of Code Inspection and Test-Driven Development', 2011, 'TSE',
                      'Wilkerson, J. W.; Nunamaker, J. F.; Mercer, R.',
                      ['Wohlin et al.'], 'Home')
    #e.median_task_duration = 2
    e.median_experiment_duration = 14
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='two-by-two, between-subjects, factorial design',
                        explicity=1, treatmentQuantity=4, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='form')

    createStatistics(
        e, 0, 'Bartlett’s test; MANOVA')

    s = createSampling('Reward', e)

    addProfile(newProfile='Undergradstudent', newQuantity=29, sample=s)


def createPaper42():
    e = newExperiment('Descriptive Compound Identifier Names Improve Source Code Comprehension', 2018, 'ICSE',
                      'Schankin, A.; Berger, A.; Holt, D. V.; Hofmeister, J. C.; Riedel, T.; Beigl, M. ',
                      [], 'Home')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 14
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='DEGUGGING', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')

    createStatistics(
        e, 1, 'Cohen’s d; t-test')

    s = createSampling('Not Clear', e)

    addProfile(newProfile='Student', newQuantity=50, sample=s)
    addProfile(newProfile='Professionals', newQuantity=38, sample=s)


def createPaper43():
    e = newExperiment('Drag-and-Drop Refactoring: Intuitive and Efficient Program Transformation', 2013, 'ICSE',
                      'Lee, Y. Y.; Chen, N.; Johnson, R. E.',
                      [], 'Home')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 14
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=9, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='screen recorder')

    createStatistics(
        e, 0, 'Wilcoxon Signed Rank Test')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='CONSTRUCTION; DEGUGGING; COMPREHENSION', newQuantity=3, experiment=e)

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
                      ['Wohlin et al.'], 'Home')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 14
    # attachDesign(e, '4-group crossover')
    setExperimentDesign(newDesign='complete block design',
                        explicity=0, treatmentQuantity=3, experiment=e, normalizedDesing='4-group crossover')
    addTask(newTaskType='COMPREHENSION', newQuantity=4, experiment=e)
    addTask(newTaskType='COMPREHENSION', newQuantity=4, experiment=e)
    addTask(newTaskType='COMPREHENSION', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='tool')

    createStatistics(
        e, 1, 'Kruskal-Wallis test; Cliff’s δ effect')

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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='crossover design',
                        explicity=1, treatmentQuantity=3, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='CONSTRUCTION', newQuantity=17, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=17, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE',
                   instrument='tool')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='tool')

    createStatistics(
        e, 1, 't-test; Spearman rho; Fisher`s exact test')

    s = createSampling('Voluntiers', e)
    #addCharacteristic(newCharac='gender', sample=s)

    addProfile(newProfile='Professionals', newQuantity=65, sample=s)


def createPaper48():
    e = newExperiment('Exploiting Dynamic Information in IDEs Improves Speed and Correctness of Software Maintenance Tasks', 2012, 'TSE',
                      'Rothlisberger, D.; Harry, M.; Binder, W.; Moret, P.; Ansaloni, D.; Villazon, A.; Nierstrasz, O.',
                      [], 'Company')
    e.median_task_duration = 2
    #e.median_experiment_duration = 2
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='MAINTENANCE', newQuantity=5, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE',
                   instrument='form')
    addMeasuriment(experiment=e, newMeasure='TIME',
                   instrument='Experimenter')

    createStatistics(
        e, 0, 'Kolmogorov-Smirnov test; Levene test; Student’s t-test')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='between-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE; CONSTRUCTION', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')
    addMeasuriment(experiment=e, newMeasure='CODE')

    createStatistics(
        e, 0, 'Wilcoxon Signed Rank Test; t-test')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)
    addCharacteristic(newCharac='age', sample=s)
    addCharacteristic(newCharac='Java Experience', sample=s)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Student', newQuantity=12, sample=s)

def createPaper50():
    e = newExperiment('An External Replication on the Effects of Test-driven Development Using a Multi-site Blind Analysis Approach'
                      , 2015, 'ICSE',
                      'Fucci, D.; Scanniello, G.; Romano, S.; Shepperd, M.; Sigweni, B.; Uyaguari, F.; Oivo, M.',
                      [], 'Laboratory')
    e.median_task_duration = 3
    #e.median_experiment_duration = 2
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='Balanced crossover design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='CONSTRUCTION', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')

    createStatistics(
        e, 0, 'non-directional one-sample sign test; Kruskal-Wallis test; Cliff’s δ effect')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='Professional Experience', sample=s)
    addCharacteristic(newCharac='JUnit Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=21, sample=s)

def createPaper51():
    e = newExperiment('CodeHint: Dynamic and Interactive Synthesis of Code Snippets'
                      , 2014, 'ICSE',
                      'Galenson, J.; Reames, P.; Bodik, R.; Hartmann, B.; Sen, K.',
                      [], 'Laboratory')
    #e.median_task_duration = 3
    #e.median_experiment_duration = 2
    # attachDesign(e, '4-group crossover')
    setExperimentDesign(newDesign='within-subjects counterbalanced',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='4-group crossover')
    addTask(newTaskType='MAINTENANCE', newQuantity=5, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=5, experiment=e)
    addTask(newTaskType='MAINTENANCE', newQuantity=5, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(
        e, 0, 't-test; chi-squared tests')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='Professional Experience', sample=s)s

    addProfile(newProfile='Gradstudent', newQuantity=12, sample=s)
    addProfile(newProfile='Undergradstudent', newQuantity=2, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    # attachDesign(e2, '4-group crossover')
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e2, normalizedDesing='4-group crossover')
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='TIME')
    addMeasuriment(experiment=e2, newMeasure='CODE')
    createStatistics(
        e2, 0, 't-test; chi-squared tests')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Mann-Whitney test')

    s = createSampling('Paid', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)
    addCharacteristic(newCharac='Java Experience', sample=s)
    addCharacteristic(newCharac='C# Experience', sample=s)
    addCharacteristic(newCharac='Refactoring Experience', sample=s)

    addProfile(newProfile='Student', newQuantity=6, sample=s)
    addProfile(newProfile='Professionals', newQuantity=2, sample=s)

def createPaper53():
    e = newExperiment('Does syntax highlighting help programming novices?', 2018, 'ESE',
                      'Hannebauer, C.; Hesenius, M.; Gruhn, V.',
                      [], 'Laboratory')
    e.median_task_duration = 1
    #e.median_experiment_duration = 2
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='COMPREHENSION', newQuantity=20, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')

    createStatistics(
        e, 1, 'x2 test; Barnard’s Exact Test; Fisher`s exact test')

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
    # attachDesign(e, '4-group crossover')
    setExperimentDesign(newDesign='within-subjects balanced design',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='4-group crossover')
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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='Latin Square design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE' , instrument = 'tool')
    addMeasuriment(experiment=e, newMeasure='TIME' , instrument = 'tool')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE' , instrument = 'screen recorder')

    createStatistics(e, 0, 'ANOVA; Bartlett’s test; Box Cox; Tukey tests')

    s = createSampling('Voluntiers', e)
    #addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=10, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    # attachDesign(e2, 'crossover design')
    setExperimentDesign(newDesign='Latin Square design',
                        explicity=1, treatmentQuantity=2, experiment=e2, normalizedDesing='crossover design')
    #e2.median_task_duration = 2
    addTask(newTaskType='COMPREHENSION', newQuantity=4, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='CODE' , instrument = 'tool')
    addMeasuriment(experiment=e2, newMeasure='TIME' , instrument = 'tool')
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE' , instrument = 'screen recorder')
    createStatistics(
        e2, 0, 'ANOVA; Bartlett’s test; Box Cox; Tukey tests')

    s2 = createSampling('Voluntiers', e2)
    addProfile(newProfile='Undergradstudent', newQuantity=14, sample=s2)


def createPaper59():
    e = newExperiment('Are Students Representatives of Professionals in Software Engineering Experiments?'
                      , 2014, 'ICSE',
                      'Salman, I.; Misirli, A. T.; Juristo, N.',
                      [], 'Laboratory')
    e.median_task_duration = 1.5
    #e.median_experiment_duration = 2
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='one-factor two-level, within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='CONSTRUCTION', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE' , instrument = 'tool')

    createStatistics(e, 0, 'Kolmogorov-Smirnov test')

    s = createSampling('Part of Course', e)
    addCharacteristic(newCharac='nationality', sample=s)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=17, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    # attachDesign(e2, 'crossover design')
    setExperimentDesign(newDesign='one-factor two-level, within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e2, normalizedDesing='crossover design')
    #e2.median_task_duration = 2
    addTask(newTaskType='CONSTRUCTION', newQuantity=3, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='CODE' , instrument = 'tool')
    createStatistics(
        e2, 0, 'Kolmogorov-Smirnov test')

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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='COMPREHENSION', newQuantity=3, experiment=e)

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='between-subject design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME' , instrument = 'tool')

    createStatistics(e, 0, 'Shapiro-Wilk test; Mann-Whitney test')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='randomized block design',
                        explicity=1, treatmentQuantity=4, experiment=e, normalizedDesing='Independent groups')
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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='repeated measures with cross-over experimental design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='CONSTRUCTION', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')
    addMeasuriment(experiment=e, newMeasure='Others' , details='test coverage')

    createStatistics(e, 0, 'Shapiro-Wilk test; Wilcoxon Signed Rank Test; Mann-Whitney test')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='gender', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=46, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    # attachDesign(e2, 'crossover design')
    setExperimentDesign(newDesign='repeated measures with cross-over experimental design',
                        explicity=1, treatmentQuantity=2, experiment=e2, normalizedDesing='crossover design')
    #e2.median_task_duration = 2
    addTask(newTaskType='CONSTRUCTION', newQuantity=6, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='TIME')
    addMeasuriment(experiment=e2, newMeasure='Others' , details='test coverage')
    createStatistics(
        e2, 0, 'Shapiro-Wilk test; Wilcoxon Signed Rank Test; Mann-Whitney test')

    s2 = createSampling('Not Clear', e2)

    addProfile(newProfile='Undergradstudent', newQuantity=39, sample=s2)

    # experiment 3
    e3 = addExperiment(e, newSettings='Laboratory')
    # attachDesign(e3, 'crossover design')
    setExperimentDesign(newDesign='repeated measures with cross-over experimental design',
                        explicity=1, treatmentQuantity=2, experiment=e3, normalizedDesing='crossover design')
    #e2.median_task_duration = 2
    addTask(newTaskType='CONSTRUCTION', newQuantity=6, experiment=e3)
    addMeasuriment(experiment=e3, newMeasure='TIME')
    addMeasuriment(experiment=e3, newMeasure='Others' , details='test coverage')
    createStatistics(
        e3, 0, 'Shapiro-Wilk test; Wilcoxon Signed Rank Test; Mann-Whitney test')

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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='2x2 randomized between-subject factorial design',
                        explicity=1, treatmentQuantity=3, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')
    addMeasuriment(experiment=e, newMeasure='Others' , instrument = 'number of switches')

    createStatistics(e, 1, 'Shapiro-Wilk test; T-Test; ANOVA; Levene Test')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=4, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form', details='TAM, self-estimation and diaries')

    createStatistics(e, 0, 'Wilcoxon Signed Rank Test; Cronbach’s Alpha reliability level')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='programming experience', sample=s)
    addCharacteristic(newCharac='programming laguages', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=14, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    # attachDesign(e2, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=4, experiment=e2, normalizedDesing='Independent groups')
    #e2.median_task_duration = 2
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE', instrument='form', details='TAM, self-estimation and diaries')

    createStatistics(
        e2, 0, 'Wilcoxon Signed Rank Test; Cronbach’s Alpha reliability level')

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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='within-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='CONSTRUCTION', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')
    addMeasuriment(experiment=e, newMeasure='CODE')

    createStatistics(e, 1, 'Wilcoxon Signed Rank Test')

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
    # attachDesign(e, 'Pretest and posttest control')
    setExperimentDesign(newDesign='partially counter-balanced repeated measures design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Pretest and posttest control')
    addTask(newTaskType='REVIEW', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='tool')

    createStatistics(e, 1, 'Wilcoxon Signed Rank Test; ANOVA')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=3, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')
    addMeasuriment(experiment=e, newMeasure='Others', instrument='repository', details='resolve conflicts')

    createStatistics(e, 1, 'x2 test')

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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='one factor and two treatments with two blocking variables',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='TEST', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')

    createStatistics(e, 0, 'ANOVA; Pearson P test; Shapiro-Wilk test')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=3, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, '')

    s = createSampling('Part of Course', e)
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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='CONSTRUCTION', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 0, 'Kendall’s methodology')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Programming Experience', sample=s)

    addProfile(newProfile='Gradstudent', newQuantity=8, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    # attachDesign(e2, 'Independent groups')
    setExperimentDesign(newDesign='factorial design',
                        explicity=1, treatmentQuantity=4, experiment=e2, normalizedDesing='Independent groups')
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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=3, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=4, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Kolmogorov-Smirnov test; Shapiro-Wilk test; Mann-Whitney test')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='between-group user study',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE; COMPREHENSION', newQuantity=3, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 't-test; Kolmogorov-Smirnov test; Exact Bootstrap')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='Java Experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=1, sample=s)
    addProfile(newProfile='Gradstudent', newQuantity=9, sample=s)

def createPaper74():
    e = newExperiment('Labeling source code with information retrieval methods: an empirical study'
                      , 2014, 'ESE',
                      'De Lucia, A.; Di Penta, M.; Oliveto, R.; Panichella, A.; Panichella, S.',
                      [], 'Home')
    #e.median_task_duration = 1
    e.median_experiment_duration = 14
    # attachDesign(e, 'Pretest and posttest control')
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=4, experiment=e, normalizedDesing='Pretest and posttest control')
    addTask(newTaskType='COMPREHENSION', newQuantity=10, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 1, 'Wilcoxon Signed Rank Test; Holm’s correction procedure; Baker')

    s = createSampling('Not Clear', e)
    addCharacteristic(newCharac='Java Experience', sample=s)
    addCharacteristic(newCharac='Professional Experience', sample=s)
    addCharacteristic(newCharac='Years programming', sample=s)

    addProfile(newProfile='Undergradstudent', newQuantity=17, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Home')
    setExperimentDesign(newDesign='factorial design',
                        explicity=0, treatmentQuantity=4, experiment=e2, normalizedDesing='Pretest and posttest control')
    #e2.median_task_duration = 2
    e2.median_experiment_duration = 14
    addTask(newTaskType='COMPREHENSION', newQuantity=10, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e2, newMeasure='TIME')

    createStatistics(
        e2, 1, 'Wilcoxon Signed Rank Test; Holm’s correction procedure; Baker')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='unbalanced design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', details= 'Test Coverage')

    createStatistics(e, 1, 'MANCOVA; Kolmogorov-Smirnov test; Shapiro-Wilk test; square root transformation; Levene test; Pillai’s trace; Wilk’s lambda; Hotelling’s trace; Roy’s largest root')

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
    # attachDesign(e, '4-group crossover')
    setExperimentDesign(newDesign='Latin Square',
                        explicity=1, treatmentQuantity=3, experiment=e, normalizedDesing='4-group crossover')
    addTask(newTaskType='DEGUGGING', newQuantity=9, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')

    createStatistics(e, 0, 'ANOVA; Box Cox; Bartlett’s test; Tukey tests')

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
    # attachDesign(e, '4-group crossover')
    setExperimentDesign(newDesign='two-way mixed model ANOVA design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='4-group crossover')
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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
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

# def createPaper79():
#     e = newExperiment('An Empirical Study on the Impact of C++ Lambdas and Programmer Experience'
#                       , 2013, 'IST',
#                       'Mäntylä, M. V.; Itkonen, J.',
#                       [], 'Laboratory')
#     #e.median_task_duration = 4
#     e.median_experiment_duration = 30
#     setExperimentDesign(newDesign='Paired Comparison Design',
#                         explicity=0, treatmentQuantity=2, experiment=e)
#     addTask(newTaskType='TEST', newQuantity=2, experiment=e)

#     addMeasuriment(experiment=e, newMeasure='CODE')
#     addMeasuriment(experiment=e, newMeasure='TIME')

#     createStatistics(e, 0, 'F-Score')

#     s = createSampling('Not Clear', e)
#     addCharacteristic(newCharac='credit', sample=s)
#     addCharacteristic(newCharac='years of Study', sample=s)
#     addCharacteristic(newCharac='Programming Experience', sample=s)
#     addCharacteristic(newCharac='Test Experience', sample=s)

#     addProfile(newProfile='Gradstudent', newQuantity=130, sample=s)

def createPaper80():
    e = newExperiment('An Experimental Evaluation of Test Driven Development vs. Test-Last Development with Industry Professionals'
                      , 2014, 'EASE',
                      'Munir, H.; Wnuk, K.; Petersen, K.; Moayyed, M.',
                      [], 'Laboratory')
    #e.median_task_duration = 4
    e.median_experiment_duration = 30
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='email')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='email')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 1, 'Shapiro-Wilk test; Mann-Whitney test; T-test')

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
    # attachDesign(e, 'Pretest and posttest control')
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Pretest and posttest control')
    addTask(newTaskType='TEST', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', details='code and test')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='form')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 0, 'Shapiro-Wilk test; Wilcoxon Signed Rank Test; two-way permutation test')

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
    # attachDesign(e, 'Pretest and posttest control')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=6, experiment=e, normalizedDesing='Pretest and posttest control')
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='repository')

    createStatistics(e, 0, 'Pearson P test')

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
    # attachDesign(e, 'Pretest and posttest control')
    setExperimentDesign(newDesign='Factorial Design',
                        explicity=0, treatmentQuantity=6, experiment=e, normalizedDesing='Pretest and posttest control')
    addTask(newTaskType='DEGUGGING', newQuantity=10, experiment=e)

    addMeasuriment(experiment=e, newMeasure='TIME', instrument='tool')
    addMeasuriment(experiment=e, newMeasure='Others',
                   instrument='eye traker')

    createStatistics(e, 0, 't-test; Chi-squared Tests')

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
    # attachDesign(e, '4-group crossover')
    setExperimentDesign(newDesign='paired design one factor and two treatments',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='4-group crossover')
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)
    addTask(newTaskType='CONSTRUCTION', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 0, 'Wilcoxon Signed Rank Test; Mann-Whitney test; Holm’s correction; ANOVA')

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
    # attachDesign(e, 'Pretest and posttest control')
    setExperimentDesign(newDesign='Paired Comparison Design',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='Pretest and posttest control')
    addTask(newTaskType='MAINTENANCE', newQuantity=2, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE')
    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 1, 'Shapiro-Wilk test; Wilcoxon Signed Rank Test; ANOVA')

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
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='cross validation experimental design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='COMPREHENSION', newQuantity=5, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE', instrument='form')

    createStatistics(e, 0, 'ANOVA; t-test; x2 test')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='between-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=6, experiment=e)

    addMeasuriment(experiment=e, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e, newMeasure='TIME')

    createStatistics(e, 0, 'Shapiro-Wilk test; F-test; T-test; Mann-Whitney test')

    s = createSampling('Voluntiers', e)
    addCharacteristic(newCharac='Java experience', sample=s)

    addProfile(newProfile='Student', newQuantity=35, sample=s)

    # experiment 2
    e2 = addExperiment(e, newSettings='Laboratory')
    setExperimentDesign(newDesign='between-subjects design',
                        explicity=1, treatmentQuantity=2, experiment=e2, normalizedDesing='Independent groups')
    e2.median_task_duration = 2
    #e2.median_experiment_duration = 14
    addTask(newTaskType='CONSTRUCTION', newQuantity=10, experiment=e2)
    addMeasuriment(experiment=e2, newMeasure='SUBJECTIVE')
    addMeasuriment(experiment=e2, newMeasure='TIME')

    createStatistics(
        e2, 1, 'Fisher`s exact test; Mann-Whitney test')

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
    # attachDesign(e, '4-group crossover')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=2, experiment=e, normalizedDesing='4-group crossover')
    addTask(newTaskType='REVIEW', newQuantity=3, experiment=e)

    addMeasuriment(experiment=e, newMeasure='Others', details='MRI scanner data')

    createStatistics(e, 1, 'Wilcoxon Signed Rank Test')

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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=5, experiment=e, normalizedDesing='Independent groups')
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
    # attachDesign(e, 'Independent groups')
    setExperimentDesign(newDesign='between-subjects experiment design',
                        explicity=1, treatmentQuantity=2, experiment=e, normalizedDesing='Independent groups')
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='repository')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='screen recorder')

    createStatistics(e, 1, 'Shapiro-Wilk test; ANOVA; MANOVA; Bonferroni p-value correction')

    s = createSampling('Not Clear', e)
    #addCharacteristic(newCharac='Professional experience', sample=s)

    addProfile(newProfile='Professionals', newQuantity=90, sample=s)

def createPaper91():
    e = newExperiment('Decoding the representation of code in the brain: An fMRI study of code review and expertise'
                      , 2017, 'ICSE',
                      'Floyd, B.; Santander, T.; Weimer, W.',
                      [], 'Laboratory')
    #e.median_task_duration = 2
    #e.median_experiment_duration = 2
    # attachDesign(e, 'crossover design')
    setExperimentDesign(newDesign='',
                        explicity=0, treatmentQuantity=3, experiment=e, normalizedDesing='crossover design')
    addTask(newTaskType='MAINTENANCE', newQuantity=1, experiment=e)

    addMeasuriment(experiment=e, newMeasure='CODE', instrument='repository')
    addMeasuriment(experiment=e, newMeasure='TIME', instrument='screen recorder')

    createStatistics(e, 1, 'Shapiro-Wilk test; ANOVA; MANOVA; Bonferroni p-value correction')

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
    createPaper9()
    createPaper10()
    createPaper12()
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
    # createPaper79()
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
    app.run(host='0.0.0.0')

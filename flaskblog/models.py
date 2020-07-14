from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
from flaskblog.util import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


association_guideline = db.Table('association_guideline', db.metadata,
                                 db.Column('pub_id', db.Integer,
                                           db.ForeignKey('publication.pub_id')),
                                 db.Column('guide_id', db.Integer,
                                           db.ForeignKey('guideline.guide_id')),
                                 )


class Publication(db.Model):
    pub_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    venue = db.Column(db.String(20), nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    experiments = db.relationship("Experiment", backref="exp_pub", lazy=True)


class Guideline(db.Model):
    guide_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    referenced_by = db.relationship('Publication', secondary=association_guideline,
                                    backref=db.backref('guidelines', lazy='dynamic'))


class Experiment(db.Model):
    __tablename__ = 'experiment'
    exp_id = db.Column(db.Integer, primary_key=True)
    exp_pub_id = db.Column(db.Integer, db.ForeignKey(
        'publication.pub_id'), nullable=False)
    settings = db.Column(db.String(200))  # lab, office, other
    design = db.relationship("ExperimentDesign", uselist=False,
                             back_populates="experiment")
    median_task_duration = db.Column(db.Float)  # In hours
    median_experiment_duration = db.Column(db.Float)  # In Days
    tasks = db.relationship('Task', backref="task_parent", lazy=True)
    sample = db.relationship("Sampling", backref="exp", uselist=False)
    statistics = db.relationship("Statistics", backref="exp", uselist=False)
    measurements = db.relationship(
        'Measurement', backref='measu_parent', lazy=True)


class ExperimentDesign(db.Model):
    design_id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey(
        'experiment.exp_id'), nullable=False)
    experiment = db.relationship("Experiment", back_populates="design")
    treatment_quantity = db.Column(db.Integer, default=1)
    design_description = db.Column(db.String(100))
    is_explicity_design = db.Column(db.Integer, default=0)


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_parent_id = db.Column(db.Integer, db.ForeignKey(
        'experiment.exp_id'), nullable=False)
    task_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)


class Sampling(db.Model):
    __tablename__ = 'sampling'
    sample_id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey(
        'experiment.exp_id'), nullable=False)
    profiles = db.relationship(
        "SamplingProfile", backref="parent_profile", lazy=True)
    characteristics = db.relationship(
        "SamplingCharacteristic", backref="parent_charac", lazy=True)
    recruiting_strategies = db.relationship("Recruting", uselist=False,
                                            backref="parent_recru", lazy=True)

    def __repr__(self):
        return f"Sampling('{self.recruitment_type}', '{self.sample_size}')"

    def sample_classification(self):
        has_student = False
        has_professional = False
        total = 0
        classification = 0
        for a_profile in self.profiles:
            if (a_profile.profile == 'PROFESSIONAL'):
                has_professional = True
            else:
                has_student = True
            total += a_profile.quantity
        if (has_student and has_professional):
            return 'mix', total
        elif (has_professional):
            return 'professional_only', total
        else:
            return 'student_only', total


class Recruting(db.Model):
    __tablename__ = 'recruting'
    recruting_id = db.Column(db.Integer, primary_key=True)
    recruiting_strategy = db.Column(db.String(100), nullable=False)
    parent_recru_id = db.Column(db.Integer, db.ForeignKey(
        'sampling.sample_id'), nullable=False)


class SamplingProfile(db.Model):
    __tablename__ = 'sampling_profile'
    sample_profile_id = db.Column(db.Integer, primary_key=True)
    parent_profile_id = db.Column(
        db.Integer, db.ForeignKey('sampling.sample_id'), nullable=False)
    profile = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class SamplingCharacteristic(db.Model):
    __tablename__ = 'sampling_charac'
    charac_id = db.Column(db.Integer, primary_key=True)
    parent_charac_id = db.Column(
        db.Integer, db.ForeignKey('sampling.sample_id'), nullable=False)
    charac = db.Column(db.String(20), nullable=False)


class Measurement(db.Model):
    __tablename__ = 'measurement'
    measurement_id = db.Column(db.Integer, primary_key=True)
    exp_measu_id = db.Column(db.Integer, db.ForeignKey(
        'experiment.exp_id'), nullable=False)
    measurement_type = db.Column(db.String(20), nullable=False)
    measurement_details = db.Column(db.String(20))
    measurement_instruments = db.Column(db.String(100))


class Statistics(db.Model):
    __tablename__ = 'statistics'
    stat_id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey(
        'experiment.exp_id'), nullable=False)
    statistic_details = db.Column(db.String(200))
    has_power = db.Column(db.Integer, default=0)

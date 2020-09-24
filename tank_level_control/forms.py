from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import DataRequired, NumberRange


class NormalPidForm(FlaskForm):
    given_level = FloatField(u'Zadany poziom cieczy', validators=[DataRequired(), NumberRange(0)], default=50)
    tank_area = FloatField(u'Pole podstawy zbiornika', validators=[DataRequired(), NumberRange(0)], default=50)
    start_level = FloatField(u'Początkowy poziom cieczy', validators=[DataRequired(), NumberRange(0)],
                             default=10)
    time = FloatField(u'Czas symulacji', validators=[DataRequired(), NumberRange(0)], default=100)
    step = FloatField(u'Rozdzielczość symulacji', validators=[DataRequired(), NumberRange(0)], default=0.1)
    outputFactor = FloatField(
        u'Współczynnik wypływu cieczy',
        validators=[DataRequired(), NumberRange(0)], default=80,
        description='Objętość cieczy wylatującej w 1s przy wysokości słupa cieczy 1')
    Kp = FloatField(u'Kp', validators=[], default=21000)
    Ki = FloatField(u'Ki', validators=[], default=0.8)
    Kd = FloatField(u'Kd', validators=[], default=0.2)

    submit = SubmitField(u'Wprowadź dane')


class QualityOptimizationPid(FlaskForm):
    given_level = FloatField(u'Zadany poziom cieczy', validators=[DataRequired(), NumberRange(0)], default=50)
    tank_area = FloatField(u'Pole podstawy zbiornika', validators=[DataRequired(), NumberRange(0)], default=50)
    start_level = FloatField(u'Początkowy poziom cieczy', validators=[DataRequired(), NumberRange(0)],
                             default=10)
    time = FloatField(u'Czas symulacji', validators=[DataRequired(), NumberRange(0)], default=100)
    step = FloatField(u'Rozdzielczość symulacji', validators=[DataRequired(), NumberRange(0)], default=0.1)
    outputFactor = FloatField(
        u'Współczynnik wypływu cieczy',
        validators=[DataRequired(), NumberRange(0)], default=80,
        description='Objętość cieczy wylatującej w 1s przy wysokości słupa cieczy 1')
    choices = [(1, 'Klasyczny pid'), (2, 'IAE'),  (3, 'ISE'),  (4, 'ITAE'),  (5, 'ITSE')]
    testField = SelectField(u'Wskaźniki jakości', choices=choices, validators=[])
    Kp = FloatField(u'Kp', validators=[], default=1000)
    Ki = FloatField(u'Ki', validators=[], default=2)
    Kd = FloatField(u'Kd', validators=[], default=1)

    submit = SubmitField(u'Wprowadź dane')


class FuzzyController(FlaskForm):
    given_level = FloatField(u'Zadany poziom cieczy', validators=[DataRequired(), NumberRange(0)], default=50)
    tank_area = FloatField(u'Pole podstawy zbiornika', validators=[DataRequired(), NumberRange(0)], default=50)
    start_level = FloatField(u'Początkowy poziom cieczy', validators=[DataRequired(), NumberRange(0)],
                             default=10)
    time = FloatField(u'Czas symulacji', validators=[DataRequired(), NumberRange(0)], default=100)
    step = FloatField(u'Rozdzielczość symulacji', validators=[DataRequired(), NumberRange(0)], default=0.1)
    outputFactor = FloatField(
        u'Współczynnik wypływu cieczy',
        validators=[DataRequired(), NumberRange(0)], default=80,
        description='Objętość cieczy wylatującej w 1s przy wysokości słupa cieczy 1')

    submit = SubmitField(u'Wprowadź dane')

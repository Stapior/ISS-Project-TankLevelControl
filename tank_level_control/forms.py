from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.fields.html5 import *
from wtforms.validators import DataRequired, NumberRange


class NormalPidForm(FlaskForm):
    given_level = FloatField(u'Zadany poziom cieczy', validators=[DataRequired(), NumberRange(0)], default=50)
    tank_r = FloatField(u'Promień zbiornika', validators=[DataRequired(), NumberRange(0)], default=50)
    start_level = FloatField(u'Początkowy poziom cieczy', validators=[DataRequired(), NumberRange(0)],
                               default=50)
    time = FloatField(u'Czas symulacji', validators=[DataRequired(), NumberRange(0)], default=50)
    step = FloatField(u'Rozdzielczość symulacji', validators=[DataRequired(), NumberRange(0)], default=0.1)
    outputFactor = FloatField(
        u'Współczynnik wypływu cieczy',
        validators=[DataRequired(), NumberRange(0)], default=20,
        description='Objetość cieczy wylatującej w 1s przy wysokosci słupa cieczy 1')
    Kp = FloatField(u'Kp', validators=[DataRequired(), NumberRange(0)], default=100)
    Ki = FloatField(u'Ki', validators=[DataRequired(), NumberRange(0)], default=2)
    Kd = FloatField(u'Kd', validators=[DataRequired(), NumberRange(0)], default=1)

    submit = SubmitField(u'Wprowadź dane')

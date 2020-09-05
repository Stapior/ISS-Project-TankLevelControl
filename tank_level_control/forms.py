from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.fields.html5 import *
from wtforms.validators import DataRequired, NumberRange


class NormalPidForm(FlaskForm):
    tank_h = IntegerField(u'Wysokość zbiornika', validators=[DataRequired(), NumberRange(0, 100)], default=100)
    tank_r = IntegerField(u'Promień zbiornika', validators=[DataRequired(), NumberRange(0, 100)], default=50)
    hole_r = IntegerField(u'Promień otworu spustowego', validators=[DataRequired(), NumberRange(0, 100)], default=10)
    given_level = IntegerField(u'Zadany poziom cieczy', validators=[DataRequired(), NumberRange(0, 100)], default=50)
    start_level = IntegerField(u'Początkowy poziom cieczy', validators=[DataRequired(), NumberRange(0, 100)], default=50)

    submit = SubmitField(u'Wprowadź dane')

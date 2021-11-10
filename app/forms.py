from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, StringField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired
from datetime import datetime
from dateutil.relativedelta import relativedelta

one_yr_ago = datetime.now() - relativedelta(years=1)
    

class StockForm(FlaskForm):
    stock = SelectField(u'Programming Language', choices=[], validators=[DataRequired()])
    from_date = DateField('From date', format='%Y-%m-%d', default=one_yr_ago, validators=[DataRequired()])
    to_date = DateField('To date',format='%Y-%m-%d', default=datetime.today(), validators=[DataRequired()])
    submit = SubmitField('Submit')


class ModelForm(FlaskForm):
    stock = SelectField(u'Programming Language', choices=[], validators=[DataRequired()])
    model = SelectField(u'Model', choices=[('CNN', 'CNN'), ('LSTM', 'LSTM')], validators=[DataRequired()])
    
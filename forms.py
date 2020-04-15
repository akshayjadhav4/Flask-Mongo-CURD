from flask_wtf import FlaskForm
from wtforms import StringField ,IntegerField, SubmitField 
from wtforms.validators import DataRequired , Length , Email 

class StudentForm(FlaskForm):
    fullName = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    phoneNumber = IntegerField('Phone Number',validators=[DataRequired()])
    submit = SubmitField('Add Data')
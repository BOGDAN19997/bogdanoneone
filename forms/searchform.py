from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators


class CreateQuery(FlaskForm):

    nameOfCommand_List = StringField("nameOfCommand_List: ", [validators.DataRequired("Please enter your nameOfCommand_List.")])
    Expansion = StringField("Expansion: ", [validators.DataRequired("Please enter your Expansion.")])
    submit = SubmitField("Search")


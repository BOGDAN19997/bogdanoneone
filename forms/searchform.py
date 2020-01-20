from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators


class CreateQuery(FlaskForm):

    taglist_checkOfCommand_List = StringField("taglist_checkOfCommand_List: ", [validators.DataRequired("Please enter your taglist_checkOfCommand_List.")])
    Expansion = StringField("Expansion: ", [validators.DataRequired("Please enter your Expansion.")])
    submit = SubmitField("Search")


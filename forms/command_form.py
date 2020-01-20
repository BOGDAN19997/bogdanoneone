from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms import validators


class CreateCommand(FlaskForm):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter command Name.")

    ])
    command_text = StringField("Text: ", [
        validators.DataRequired("Please enter command Text.")

    ])

    expansion = StringField("Expansion: ", [
        validators.DataRequired("Please enter command Count Of Expansion.")

    ])
    versions = StringField("Versions: ", [
        validators.DataRequired("Please enter command Versions.")

    ])
    rating = FloatField("Rating: ", [
        validators.DataRequired("Please enter command Rating.")

    ])
    command_list_id = IntegerField("Command_List id: ", [
        validators.DataRequired("Please enter command Command_List id.")

    ])
    submit = SubmitField("Save")


class EditCommand(FlaskForm):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter command Name.")

    ])
    command_text = StringField("Text: ", [
        validators.DataRequired("Please enter command Text.")

    ])
    versions = StringField("Versions: ", [
        validators.DataRequired("Please enter command Versions.")

    ])
    rating = FloatField("Rating: ", [
        validators.DataRequired("Please enter command Rating.")

    ])
    submit = SubmitField("Save")
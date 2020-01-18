from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms import validators


class CreateFile(FlaskForm):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter file Name.")

    ])
    file_text = StringField("Text: ", [
        validators.DataRequired("Please enter file Text.")

    ])

    expansion = StringField("Expansion: ", [
        validators.DataRequired("Please enter file Count Of Expansion.")

    ])
    versions = StringField("Versions: ", [
        validators.DataRequired("Please enter file Versions.")

    ])
    rating = FloatField("Rating: ", [
        validators.DataRequired("Please enter file Rating.")

    ])
    command_list_id = IntegerField("Command_List id: ", [
        validators.DataRequired("Please enter file Command_List id.")

    ])
    submit = SubmitField("Save")


class EditFile(FlaskForm):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter file Name.")

    ])
    file_text = StringField("Text: ", [
        validators.DataRequired("Please enter file Text.")

    ])
    versions = StringField("Versions: ", [
        validators.DataRequired("Please enter file Versions.")

    ])
    rating = FloatField("Rating: ", [
        validators.DataRequired("Please enter file Rating.")

    ])
    submit = SubmitField("Save")
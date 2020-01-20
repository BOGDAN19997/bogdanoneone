from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms import validators


class CreateCommand(FlaskForm):
    taglist_check = StringField("Taglist check: ", [
        validators.DataRequired("Please enter command taglist check.")

    ])
    command_body = StringField("Text: ", [
        validators.DataRequired("Please enter command text.")

    ])

    expansion = StringField("Expansion: ", [
        validators.DataRequired("Please enter count of expansions in current command.")

    ])
    versions = StringField("Versions: ", [
        validators.DataRequired("Please enter versions where command was added.")

    ])
    rating = FloatField("Rating: ", [
        validators.DataRequired("Please enter command decode rating.")

    ])
    command_list_id = IntegerField("Command List id: ", [
        validators.DataRequired("Please enter command id in Command List.")

    ])
    submit = SubmitField("Save")


class EditCommand(FlaskForm):
    taglist_check = StringField("Taglist check: ", [
        validators.DataRequired("Please enter command taglist check.")

    ])
    command_body = StringField("Text: ", [
        validators.DataRequired("Please enter command text.")

    ])
    versions = StringField("Versions: ", [
        validators.DataRequired("Please enter versions where command was added.")

    ])
    rating = FloatField("Rating: ", [
        validators.DataRequired("Please enter command decode rating.")

    ])
    submit = SubmitField("Save")
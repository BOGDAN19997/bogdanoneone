from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators


class CreateVoice_Pattern(FlaskForm):
    voice_body = StringField("Voice_body: ", [
        validators.DataRequired("Please enter your Voice_body.")

    ])
    voice_data = StringField("Voice_data: ", [
        validators.DataRequired("Please enter your Voice_data.")

    ])

    email = StringField("Email: ", [
        validators.DataRequired("Please enter your Email.")

    ])
    lastname = StringField("Lastname: ", [
        validators.DataRequired("Please enter your Lastname.")

    ])

    firstname = StringField("Firstname: ", [
        validators.DataRequired("Please enter your Firstname.")

    ])

    submit = SubmitField("Save")


class EditVoice_Pattern(FlaskForm):
    voice_body = StringField("Voice_body: ", [
        validators.DataRequired("Please enter your Voice_body.")

    ])
    voice_data = StringField("Voice_data: ", [
        validators.DataRequired("Please enter your Voice_data.")

    ])

    email = StringField("Email: ", [
        validators.DataRequired("Please enter your Email.")

    ])
    lastname = StringField("Lastname: ", [
        validators.DataRequired("Please enter your Lastname.")

    ])

    firstname = StringField("Firstname: ", [
        validators.DataRequired("Please enter your Firstname.")

    ])

    submit = SubmitField("Save")
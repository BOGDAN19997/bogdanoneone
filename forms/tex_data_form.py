from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange


class CreateTex_data(FlaskForm):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter tex_data Name.")

    ])
    description = StringField("Description: ", [
        validators.DataRequired("Please enter tex_data Description.")

    ])


    countofcommand_lists = IntegerField("Count Of Command_Lists:: ",
                         validators=[NumberRange(min=0, message=">0"), DataRequired("Please enter your Count Of Command_Lists:.")]
                         )

    voice_pattern_id = IntegerField("Voice_Pattern id: ", [
        validators.DataRequired("Please enter tex_data Voice_Pattern id.")

    ])
    submit = SubmitField("Save")


class EditTex_data(FlaskForm):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter tex_data Name.")

    ])
    description = StringField("Description: ", [
        validators.DataRequired("Please enter tex_data Description.")

    ])

    countofcommand_lists = IntegerField("Count Of Command_Lists: ", [
        validators.DataRequired("Please enter tex_data Count Of Command_Lists.")

    ])

    submit = SubmitField("Save")
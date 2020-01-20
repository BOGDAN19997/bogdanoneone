from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange


class CreateTex_data(FlaskForm):
    taglist_check = StringField("Taglist check: ", [
        validators.DataRequired("Please enter text data taglist check.")

    ])
    full_body = StringField("Full body: ", [
        validators.DataRequired("Please enter text data full body.")

    ])


    countofcommand_lists = IntegerField("Count Of Command_Lists: ",
                         validators=[NumberRange(min=0, message=">0"), DataRequired("Please enter your count Of Command_Lists:.")]
                         )

    voice_pattern_id = IntegerField("Voice Pattern id: ", [
        validators.DataRequired("Please enter voice pattern id in current text data.")

    ])
    submit = SubmitField("Save")


class EditTex_data(FlaskForm):
    taglist_check = StringField("Taglist check: ", [
        validators.DataRequired("Please enter text data taglist check.")

    ])
    full_body = StringField("Full body: ", [
        validators.DataRequired("Please enter text data full body.")

    ])

    countofcommand_lists = IntegerField("Count Of Command Lists: ", [
        validators.DataRequired("Please enter count of Command Lists in current text data.")

    ])

    submit = SubmitField("Save")
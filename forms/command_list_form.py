from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import NumberRange, DataRequired


class CreateCommand_List(FlaskForm):
    taglist_check = StringField("Taglist check: ", [
        validators.DataRequired("Please enter command list tag check.")

    ])
    full_body = StringField("Full body: ", [
        validators.DataRequired("Please enter all commands in list.")

    ])


    countofcommands = IntegerField("Count Of Command_Lists: ",
                         validators=[NumberRange(min=0, message=">1"), DataRequired("Please enter your count Of Command_Lists:.")]
                         )
    text_data_id = IntegerField("Text data id: ", [
        validators.DataRequired("Please enter text data id in current command list.")

    ])
    submit = SubmitField("Save")


class EditCommand_List(FlaskForm):
    taglist_check = StringField("Taglist check: ", [
        validators.DataRequired("Please enter command list tag check.")

    ])
    full_body = StringField("Full body: ", [
        validators.DataRequired("Please enter all commands in list.")

    ])

    countofcommands = IntegerField("Count Of Command Lists: ",
                                validators=[NumberRange(min=0, message=">0"),
                                            DataRequired("Please enter your count Of Command_Lists:.")]
                                )

    submit = SubmitField("Save")
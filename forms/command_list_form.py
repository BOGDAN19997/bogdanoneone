from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import NumberRange, DataRequired


class CreateCommand_List(FlaskForm):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter command_list Name.")

    ])
    description = StringField("Description: ", [
        validators.DataRequired("Please enter command_list Description.")

    ])


    countoffiles = IntegerField("Count Of Command_Lists:: ",
                         validators=[NumberRange(min=0, message=">1"), DataRequired("Please enter your Count Of Command_Lists:.")]
                         )
    text_data_id = IntegerField("Tex_data id: ", [
        validators.DataRequired("Please enter command_list Tex_data id.")

    ])
    submit = SubmitField("Save")


class EditCommand_List(FlaskForm):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter command_list Name.")

    ])
    description = StringField("Description: ", [
        validators.DataRequired("Please enter command_list Description.")

    ])

    countoffiles = IntegerField("Count Of Command_Lists:: ",
                                validators=[NumberRange(min=0, message=">0"),
                                            DataRequired("Please enter your Count Of Command_Lists:.")]
                                )

    submit = SubmitField("Save")
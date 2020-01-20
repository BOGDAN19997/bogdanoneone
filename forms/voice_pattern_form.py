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

    voice_hmm = StringField("Voice_HMM: ", [
        validators.DataRequired("Please enter your Voice_HMM.")

    ])
    voice_emotion_logic_accent = StringField("Voice_emotion_logic_accent: ", [
        validators.DataRequired("Please enter your Voice_emotion_logic_accent.")

    ])

    voice_similar_words = StringField("Voice_similar_words: ", [
        validators.DataRequired("Please enter your Voice_similar_words.")

    ])

    submit = SubmitField("Save")


class EditVoice_Pattern(FlaskForm):
    voice_body = StringField("Voice_body: ", [
        validators.DataRequired("Please enter your Voice_body.")

    ])
    voice_data = StringField("Voice_data: ", [
        validators.DataRequired("Please enter your Voice_data.")

    ])

    voice_hmm = StringField("Voice_HMM: ", [
        validators.DataRequired("Please enter your Voice_HMM.")

    ])
    voice_emotion_logic_accent = StringField("Voice_emotion_logic_accent: ", [
        validators.DataRequired("Please enter your Voice_emotion_logic_accent.")

    ])

    voice_similar_words = StringField("Voice_similar_words: ", [
        validators.DataRequired("Please enter your Voice_similar_words.")

    ])

    submit = SubmitField("Save")
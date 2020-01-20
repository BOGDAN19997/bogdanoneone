from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators


class CreateVoice_Pattern(FlaskForm):
    voice_body = StringField("Voice body: ", [
        validators.DataRequired("Please enter your voice body.")

    ])
    voice_data = StringField("Voice data: ", [
        validators.DataRequired("Please enter your voice data.")

    ])

    voice_hmm = StringField("Voice HMM: ", [
        validators.DataRequired("Please enter your voice HMM.")

    ])
    voice_emotion_logic_accent = StringField("Voice emotional and logical accent: ", [
        validators.DataRequired("Please enter your emotional and logical accent.")

    ])

    voice_similar_words = StringField("Common similar words: ", [
        validators.DataRequired("Please enter your mostly common used words.")

    ])

    submit = SubmitField("Save")


class EditVoice_Pattern(FlaskForm):
    voice_body = StringField("Voice body: ", [
        validators.DataRequired("Please enter your voice body.")

    ])
    voice_data = StringField("Voice data: ", [
        validators.DataRequired("Please enter your voice data.")

    ])

    voice_hmm = StringField("Voice HMM: ", [
        validators.DataRequired("Please enter your voice HMM.")

    ])
    voice_emotion_logic_accent = StringField("Voice emotional and logical accent: ", [
        validators.DataRequired("Please enter your  emotional and logical accent.")

    ])

    voice_similar_words = StringField("Common similar words: ", [
        validators.DataRequired("Please enter your mostly common used words.")

    ])

    submit = SubmitField("Save")
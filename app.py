from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
import json
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Text, CheckConstraint, Sequence, Float, \
    UniqueConstraint
from sqlalchemy.orm import relationship
import datetime
from forms.tex_data_form import CreateTex_data, EditTex_data
from forms.command_list_form import CreateCommand_List, EditCommand_List
from forms.voice_pattern_form import CreateVoice_Pattern, EditVoice_Pattern
from forms.command_form import CreateCommand, EditCommand
from forms.searchform import CreateQuery
import plotly
import plotly.graph_objs as go
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from neupy import algorithms

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'prod'


app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://owwiyftiqxmksq:09737a44f178143dc8d174998458a0ba650d51ab42d08db12d24a44f775a26c6@ec2-3-220-86-239.compute-1.amazonaws.com:5432/d2b85aj2avnad1'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ormVoice_Patterns(db.Model):
    __tablename__ = 'voice_patterns'
    id = Column(Integer, Sequence('voice_patterns_id_seq', start=1, increment=1), primary_key=True)
    voice_body = Column(String(30), UniqueConstraint(taglist_check='voice_patterns_voice_body_key'), nullable=False)
    voice_data = Column(String(50), nullable=False)
    voice_hmm = Column(String(50), UniqueConstraint(taglist_check='voice_patterns_voice_hmm_key'), nullable=False)
    voice_emotion_logic_accent = Column(String(30))
    voice_similar_words = Column(String(30))
    pronunciation_date = Column(DateTime, default=datetime.datetime.now())
    voice_patternRelationShip = relationship("ormText_Data", back_populates="voice_pattern_Relation_Ship")


class ormText_Data(db.Model):
    __tablename__ = 'text_data'
    id = Column(Integer, Sequence('text_data_id_seq', start=1, increment=1), primary_key=True)
    taglist_check = Column(String(30), nullable=False)
    full_body = Column(Text)
    pronunciation_date = Column(DateTime, default=datetime.datetime.now())
    countofcommand_lists = Column(Integer, CheckConstraint('countofcommand_lists >= 0'), nullable=False, default=0)
    voice_pattern_id = Column(Integer, ForeignKey('voice_patterns.id'))
    voice_pattern_Relation_Ship = relationship("ormVoice_Patterns", back_populates="voice_patternRelationShip")
    text_dataRelationShip = relationship("ormCommand_List", back_populates="text_data_Relation_Ship")


class ormCommand_List(db.Model):
    __tablename__ = 'command_list'
    id = Column(Integer, Sequence('command_list_id_seq', start=1, increment=1), primary_key=True)
    taglist_check = Column(String(30), nullable=False)
    full_body = Column(Text)
    pronunciation_date = Column(DateTime, default=datetime.datetime.now())
    countofcommands = Column(Integer, CheckConstraint('countofcommands >= 0'), nullable=False, default=0)
    text_data_id = Column(Integer, ForeignKey('text_data.id'))
    text_data_Relation_Ship = relationship("ormText_Data", back_populates="text_dataRelationShip")
    commandRelationShip = relationship("ormCommands", back_populates="command_Relation_Ship")


class ormCommands(db.Model):
    __tablename__ = 'commands'
    id = Column(Integer, Sequence('commands_id_seq', start=1, increment=1), primary_key=True)
    taglist_check = Column(String(30), nullable=False)
    command_body = Column(Text)
    expansion = Column(String(10), nullable=False)
    versions = Column(String(30), nullable=False, default='1.0')
    pronunciation_date = Column(DateTime, default=datetime.datetime.now())
    rating = Column(Float)
    command_list_id = Column(Integer, ForeignKey('command_list.id'))
    command_Relation_Ship = relationship("ormCommand_List", back_populates="commandRelationShip")


@app.route('/')
def hello_world():
    text = ""
    return render_template('index.html', action="/")


@app.route('/all/voice_pattern')
def all_voice_pattern():
    taglist_check = "voice_pattern"
    voice_pattern_db = db.session.query(ormVoice_Patterns).all()
    voice_pattern = []
    for row in voice_pattern_db:
        voice_pattern.append({"id": row.id, "voice_body": row.voice_body, "voice_data": row.voice_data, "voice_hmm": row.voice_hmm,
                     "voice_emotion_logic_accent": row.voice_emotion_logic_accent, "voice_similar_words": row.voice_similar_words, "pronunciation_date": row.pronunciation_date})
    return render_template('allVoice_Pattern.html', taglist_check=taglist_check, voice_patterns=voice_pattern, action="/all/voice_pattern")


@app.route('/all/tex_data')
def all_tex_data():
    taglist_check = "tex_data"
    tex_data_db = db.session.query(ormText_Data).all()
    tex_data = []
    for row in tex_data_db:
        tex_data.append({"id": row.id, "taglist_check": row.taglist_check, "full_body": row.full_body, "pronunciation_date": row.pronunciation_date,
                           "countofcommand_lists": row.countofcommand_lists, "voice_pattern_id": row.voice_pattern_id})
    return render_template('allTex_data.html', taglist_check=taglist_check, tex_data=tex_data, action="/all/tex_data")


@app.route('/all/command_list')
def all_command_list():
    taglist_check = "command_list"
    command_list_db = db.session.query(ormCommand_List).all()
    command_list = []
    for row in command_list_db:
        command_list.append({"id": row.id, "taglist_check": row.taglist_check, "full_body": row.full_body, "pronunciation_date": row.pronunciation_date,
                        "countofcommands": row.countofcommands, "text_data_id": row.text_data_id})
    return render_template('allCommand_List.html', taglist_check=taglist_check, command_list=command_list, action="/all/command_list")


@app.route('/all/command')
def all_command():
    taglist_check = "command"
    command_db = db.session.query(ormCommands).all()
    command = []
    for row in command_db:
        command.append({"id": row.id, "taglist_check": row.taglist_check, "command_body": row.command_body, "expansion": row.expansion,
                     "versions": row.versions,
                     "pronunciation_date": row.pronunciation_date, "rating": row.rating, "command_list_id": row.command_list_id})
    return render_template('allCommand.html', taglist_check=taglist_check, command=command, action="/all/command")


@app.route('/create/voice_pattern', methods=['GET', 'POST'])
def create_voice_pattern():
    form = CreateVoice_Pattern()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_voice_pattern.html', form=form, form_name="New voice pattern", action="create/voice_pattern")
        else:

            ids = db.session.query(ormVoice_Patterns).all()
            check = True
            for row in ids:
                if row.voice_body == form.voice_body.data:
                    check = False

            new_var = ormVoice_Patterns(

                voice_body=form.voice_body.data,
                voice_data=form.voice_data.data,
                voice_hmm=form.voice_hmm.data,
                voice_emotion_logic_accent=form.voice_emotion_logic_accent.data,
                voice_similar_words=form.voice_similar_words.data,

            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_voice_pattern'))
            else:
                form.voice_body.errors = "this voice pattern already exists"

    return render_template('create_voice_pattern.html', form=form, form_name="New voice pattern", action="create/voice_pattern")


@app.route('/create/tex_data', methods=['GET', 'POST'])
def create_tex_data():
    form = CreateTex_data()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_tex_data.html', form=form, form_name="New text data",
                                   action="create/tex_data")
        else:

            ids = db.session.query(ormVoice_Patterns).all()
            check = False
            for row in ids:
                if row.id == form.voice_pattern_id.data:
                    check = True

            new_var = ormText_Data(

                taglist_check=form.taglist_check.data,
                full_body=form.full_body.data,
                countofcommand_lists=form.countofcommand_lists.data,
                voice_pattern_id=form.voice_pattern_id.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_tex_data'))

    return render_template('create_tex_data.html', form=form, form_name="New text data", action="create/tex_data")


@app.route('/create/command_list', methods=['GET', 'POST'])
def create_command_list():
    form = CreateCommand_List()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_command_list.html', form=form, form_name="New command list", action="create/command_list")
        else:

            ids = db.session.query(ormText_Data).all()
            check = False
            for row in ids:
                if row.id == form.text_data_id.data:
                    check = True

            new_var = ormCommand_List(

                taglist_check=form.taglist_check.data,
                full_body=form.full_body.data,
                countofcommands=form.countofcommands.data,
                text_data_id=form.text_data_id.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_command_list'))

    return render_template('create_command_list.html', form=form, form_name="New command list", action="create/command_list")


@app.route('/create/command', methods=['GET', 'POST'])
def create_command():
    form = CreateCommand()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_command.html', form=form, form_name="New command", action="create/command")
        else:

            ids = db.session.query(ormCommand_List).all()
            check = False
            for row in ids:
                if row.id == form.command_list_id.data:
                    check = True

            new_var = ormCommands(

                taglist_check=form.taglist_check.data,
                command_body=form.command_body.data,
                expansion=form.expansion.data,
                versions=form.versions.data,
                rating=form.rating.data,
                command_list_id=form.command_list_id.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_command'))

    return render_template('create_command.html', form=form, form_name="New command", action="create/command")


@app.route('/delete/voice_pattern', methods=['GET'])
def delete_voice_pattern():
    id = request.args.get('id')

    result = db.session.query(ormVoice_Patterns).filter(ormVoice_Patterns.id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_voice_pattern'))


@app.route('/delete/tex_data', methods=['GET'])
def delete_tex_data():
    id = request.args.get('id')

    result = db.session.query(ormText_Data).filter(ormText_Data.id == id).one()

    # db.session.delete(result)
    #
    # result = db.session.query(ormCommand_List).filter(ormCommand_List.text_data_id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_tex_data'))


@app.route('/delete/command_list', methods=['GET'])
def delete_command_list():
    id = request.args.get('id')

    result = db.session.query(ormCommand_List).filter(ormCommand_List.id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_command_list'))


@app.route('/delete/command', methods=['GET'])
def delete_command():
    id = request.args.get('id')

    result = db.session.query(ormCommands).filter(ormCommands.id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_command'))


@app.route('/edit/voice_pattern', methods=['GET', 'POST'])
def edit_voice_pattern():
    form = EditVoice_Pattern()
    id = request.args.get('id')
    if request.method == 'GET':

        voice_patterns = db.session.query(ormVoice_Patterns).filter(ormVoice_Patterns.id == id).one()

        form.voice_body.data = voice_patterns.voice_body
        form.voice_data.data = voice_patterns.voice_data
        form.voice_hmm.data = voice_patterns.voice_hmm
        form.voice_emotion_logic_accent.data = voice_patterns.voice_emotion_logic_accent
        form.voice_similar_words.data = voice_patterns.voice_similar_words

        return render_template('edit_voice_pattern.html', form=form, form_name="Edit voice pattern",
                               action="edit/voice_pattern?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_voice_pattern.html', form=form, form_name="Edit voice pattern", action="edit/voice_pattern?id=" + id)
        else:

            # find voice_pattern
            var = db.session.query(ormVoice_Patterns).filter(ormVoice_Patterns.id == id).one()
            print(var)

            # update fields from form data

            var.voice_body = form.voice_body.data
            var.voice_data = form.voice_data.data
            var.voice_hmm = form.voice_hmm.data
            var.voice_emotion_logic_accent = form.voice_emotion_logic_accent.data
            var.voice_similar_words = form.voice_similar_words.data
            db.session.commit()

            return redirect(url_for('all_voice_pattern'))


@app.route('/edit/tex_data', methods=['GET', 'POST'])
def edit_tex_data():
    form = EditTex_data()
    id = request.args.get('id')
    if request.method == 'GET':

        tex_data = db.session.query(ormText_Data).filter(ormText_Data.id == id).one()

        form.taglist_check.data = tex_data.taglist_check
        form.full_body.data = tex_data.full_body
        form.countofcommand_lists.data = tex_data.countofcommand_lists

        return render_template('edit_tex_data.html', form=form, form_name="Edit text data",
                               action="edit/tex_data?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_tex_data.html', form=form, form_name="Edit text data",
                                   action="edit/tex_data?id=" + id)
        else:

            # find voice_pattern
            var = db.session.query(ormText_Data).filter(ormText_Data.id == id).one()
            print(var)

            # update fields from form data

            var.taglist_check = form.taglist_check.data
            var.full_body = form.full_body.data
            var.countofcommand_lists = form.countofcommand_lists.data
            db.session.commit()

            return redirect(url_for('all_tex_data'))


@app.route('/edit/command_list', methods=['GET', 'POST'])
def edit_command_list():
    form = EditCommand_List()
    id = request.args.get('id')
    if request.method == 'GET':

        command_list = db.session.query(ormCommand_List).filter(ormCommand_List.id == id).one()

        form.taglist_check.data = command_list.taglist_check
        form.full_body.data = command_list.full_body
        form.countofcommands.data = command_list.countofcommands

        return render_template('edit_command_list.html', form=form, form_name="Edit command list",
                               action="edit/command_list?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_command_list.html', form=form, form_name="Edit command list", action="edit/command_list?id=" + id)
        else:

            # find voice_pattern
            var = db.session.query(ormCommand_List).filter(ormCommand_List.id == id).one()
            print(var)

            # update fields from form data

            var.taglist_check = form.taglist_check.data
            var.full_body = form.full_body.data
            var.countofcommands = form.countofcommands.data
            db.session.commit()

            return redirect(url_for('all_command_list'))


@app.route('/edit/command', methods=['GET', 'POST'])
def edit_command():
    form = EditCommand()
    id = request.args.get('id')
    if request.method == 'GET':

        command = db.session.query(ormCommands).filter(ormCommands.id == id).one()

        form.taglist_check.data = command.taglist_check
        form.command_body.data = command.command_body
        form.versions.data = command.versions
        form.rating.data = command.rating

        return render_template('edit_command.html', form=form, form_name="Edit command",
                               action="edit/command?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_command.html', form=form, form_name="Edit command", action="edit/command?id=" + id)
        else:

            # find voice_pattern
            var = db.session.query(ormCommands).filter(ormCommands.id == id).one()
            print(var)

            # update fields from form data

            var.taglist_check = form.taglist_check.data
            var.command_body = form.command_body.data
            var.versions = form.versions.data
            var.rating = form.rating.data
            db.session.commit()

            return redirect(url_for('all_command'))


@app.route('/dashboard')
def dashboard():
    query1 = (
        db.session.query(
            func.count(),
            ormCommands.expansion
        ).group_by(ormCommands.expansion)
    ).all()

    query = (
        db.session.query(
            func.count(ormVoice_Patterns.id),
            ormVoice_Patterns.pronunciation_date
        ).group_by(ormVoice_Patterns.pronunciation_date)
    ).all()

    dates, counts = zip(*query)
    bar = go.Bar(
        x=counts,
        y=dates
    )

    skills, voice_pattern_count = zip(*query1)
    pie = go.Pie(
        labels=voice_pattern_count,
        values=skills
    )
    print(dates, counts)
    print(skills, voice_pattern_count)

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)


@app.route('/clasteresation', methods=['GET', 'POST'])
def claster():
    df = pd.DataFrame()

    for taglist_check, expansion in db.session.query(ormCommand_List.taglist_check, ormCommands.expansion).join(ormCommands,
                                                                                      ormCommand_List.id == ormCommands.command_list_id):
        print(taglist_check, expansion)
        df = df.append({"taglist_check": taglist_check, "expansion": expansion}, ignore_index=True)

    X = pd.get_dummies(data=df)
    print(X)
    count_clasters = len(df['expansion'].unique())
    print(count_clasters)
    kmeans = KMeans(n_clusters=count_clasters, random_state=0).fit(X)
    # print(kmeans)
    count_columns = len(X.columns)
    test_list = [0] * count_columns
    test_list[0] = 1
    test_list[-2] = 1
    print(test_list)
    # print(kmeans.labels_)
    print(kmeans.predict(np.array([test_list])))

    query1 = (
        db.session.query(
            func.count(),
            ormCommands.expansion
        ).group_by(ormCommands.expansion)
    ).all()
    skills, voice_pattern_count = zip(*query1)
    pie = go.Pie(
        labels=voice_pattern_count,
        values=skills
    )
    data = {
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('clasteresation.html', row=kmeans.predict(np.array([test_list]))[0],
                           count_claster=count_clasters, graphsJSON=graphsJSON)


@app.route('/regretion', methods=['GET', 'POST'])
def correlation():
    df = pd.DataFrame()
    for count_proj, count_commands in db.session.query(ormText_Data.countofcommand_lists, ormCommand_List.countofcommands).join(
            ormText_Data,
            ormText_Data.id == ormCommand_List.text_data_id):
        print(count_proj, count_commands)
        df = df.append({"count_proj": float(count_proj), "count_commands": float(count_commands)}, ignore_index=True)
    db.session.close()
    scaler = StandardScaler()
    scaler.fit(df[["count_proj"]])
    train_X = scaler.transform(df[["count_proj"]])
    # print(train_X, df[["count_commands"]])
    reg = LinearRegression().fit(train_X, df[["count_commands"]])

    test_array = [[3]]
    test = scaler.transform(test_array)
    result = reg.predict(test)

    query1 = db.session.query(ormText_Data.countofcommand_lists, ormCommand_List.countofcommands).join(
            ormText_Data, ormText_Data.id == ormCommand_List.text_data_id).all()
    count_pr, count_fl = zip(*query1)
    scatter = go.Scatter(
        x=count_pr,
        y=count_fl,
        mode = 'markers',
        marker_color='rgba(255, 0, 0, 100)',
        taglist_check = "data"
    )
    x_line = np.linspace(0, 10)
    y_line = x_line * reg.coef_[0, 0] + reg.intercept_[0]
    line = go.Scatter(
        x=x_line,
        y=y_line,
        mode = 'lines',
        marker_color='rgba(0, 0, 255, 100)',
        taglist_check = "regretion"
    )
    data = [scatter, line]
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('regretion.html', row=int(round(result[0, 0])), test_data=test_array[0][0], coef=reg.coef_[0],
                           coef1=reg.intercept_, graphsJSON = graphsJSON)

@app.route('/clasification', methods=['GET', 'POST'])
def clasification():
    df = pd.DataFrame()
    for command_body, rating in db.session.query(ormCommands.command_body, ormCommands.rating):
        print(command_body, rating)
        df = df.append({"command_name": command_body, "rating": float(rating)}, ignore_index=True)
    # db.session.close()

    df['count_symbols'] = df['command_name'].apply(len)
    df.loc[df['rating'] < 0.33, 'quality'] = 0
    df.loc[df['rating'] >= 0.33, 'quality'] = 1
    print(df)
    pnn = algorithms.PNN(std=10, verbose=False)
    pnn.train(df['count_symbols'], df['quality'])

    test_data = 'ewij weioh uia guu aweg'
    t_test_data = len(test_data)
    y_predicted = pnn.predict([t_test_data])
    result = "Ні"
    if y_predicted - 1 < 0.0000000000001:
        result = "Так"

    return render_template('clasification.html', y_predicted=result, test_data=test_data)


list_event = []


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = CreateQuery()
    if request.method == 'POST':
        if not form.validate():

            return render_template('search.html', form=form, form_name="Search", action="search")
        else:
            list_event.clear()
            for id, taglist_check, Expansion in db.session.query(ormCommands.id, ormCommands.taglist_check, ormCommands.expansion
                                                        ):
                if taglist_check == form.nameOfCommand_List.data and Expansion == form.Expansion.data:
                    list_event.append(id)

            return redirect(url_for('searchList'))

    return render_template('search.html', form=form, form_name="Search", action="search")

@app.route('/search/result')
def searchList():
    res = []
    try:
        for i in list_event:
            version,rating = db.session \
                .query(ormCommands.versions, ormCommands.rating).filter(ormCommands.id == i).one()
            res.append(
                {"version": version, "rating": rating})
    except:
        print("don't data")
    print(list_event)

    return render_template('search_list_event.html', taglist_check="result", results=res, action="/search/result")
if __name__ == '__main__':
    app.run()

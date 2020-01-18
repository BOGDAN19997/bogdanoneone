from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
import json
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Text, CheckConstraint, Sequence, Float, \
    UniqueConstraint
from sqlalchemy.orm import relationship
import datetime
from forms.reposytory_form import CreateReposytory, EditReposytory
from forms.project_form import CreateProject, EditProject
from forms.user_form import CreateUser, EditUser
from forms.file_form import CreateFile, EditFile
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

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost/Joseph'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://qexacebxlyoflv:7f1848d692d8a690603199584eaf0f697e63459f365c69074da6ec8ca508e9fc@ec2-107-21-126-201.compute-1.amazonaws.com:5432/ddj3djvlda7rga'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ormUsers(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('users_id_seq', start=1, increment=1), primary_key=True)
    login = Column(String(30), UniqueConstraint(name='users_login_key'), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50), UniqueConstraint(name='users_email_key'), nullable=False)
    lastname = Column(String(30))
    firstname = Column(String(30))
    created = Column(DateTime, default=datetime.datetime.now())
    userRelationShip = relationship("ormReposytoty", back_populates="user_Relation_Ship")


class ormReposytoty(db.Model):
    __tablename__ = 'reposytoty'
    id = Column(Integer, Sequence('reposytoty_id_seq', start=1, increment=1), primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(Text)
    created = Column(DateTime, default=datetime.datetime.now())
    countofprojects = Column(Integer, CheckConstraint('countofprojects >= 0'), nullable=False, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_Relation_Ship = relationship("ormUsers", back_populates="userRelationShip")
    reposytotyRelationShip = relationship("ormProject", back_populates="reposytoty_Relation_Ship")


class ormProject(db.Model):
    __tablename__ = 'project'
    id = Column(Integer, Sequence('project_id_seq', start=1, increment=1), primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(Text)
    created = Column(DateTime, default=datetime.datetime.now())
    countoffiles = Column(Integer, CheckConstraint('countoffiles >= 0'), nullable=False, default=0)
    reposytoty_id = Column(Integer, ForeignKey('reposytoty.id'))
    reposytoty_Relation_Ship = relationship("ormReposytoty", back_populates="reposytotyRelationShip")
    fileRelationShip = relationship("ormFiles", back_populates="file_Relation_Ship")


class ormFiles(db.Model):
    __tablename__ = 'files'
    id = Column(Integer, Sequence('files_id_seq', start=1, increment=1), primary_key=True)
    name = Column(String(30), nullable=False)
    file_text = Column(Text)
    expansion = Column(String(10), nullable=False)
    versions = Column(String(30), nullable=False, default='1.0')
    created = Column(DateTime, default=datetime.datetime.now())
    rating = Column(Float)
    project_id = Column(Integer, ForeignKey('project.id'))
    file_Relation_Ship = relationship("ormProject", back_populates="fileRelationShip")


@app.route('/')
def hello_world():
    text = ""
    return render_template('index.html', action="/")


@app.route('/all/user')
def all_user():
    name = "user"
    user_db = db.session.query(ormUsers).all()
    user = []
    for row in user_db:
        user.append({"id": row.id, "login": row.login, "password": row.password, "email": row.email,
                     "lastname": row.lastname, "firstname": row.firstname, "created": row.created})
    return render_template('allUser.html', name=name, users=user, action="/all/user")


@app.route('/all/reposytory')
def all_reposytory():
    name = "reposytory"
    reposytory_db = db.session.query(ormReposytoty).all()
    reposytory = []
    for row in reposytory_db:
        reposytory.append({"id": row.id, "name": row.name, "description": row.description, "created": row.created,
                           "countofprojects": row.countofprojects, "user_id": row.user_id})
    return render_template('allReposytory.html', name=name, reposytory=reposytory, action="/all/reposytory")


@app.route('/all/project')
def all_project():
    name = "project"
    project_db = db.session.query(ormProject).all()
    project = []
    for row in project_db:
        project.append({"id": row.id, "name": row.name, "description": row.description, "created": row.created,
                        "countoffiles": row.countoffiles, "reposytoty_id": row.reposytoty_id})
    return render_template('allProject.html', name=name, project=project, action="/all/project")


@app.route('/all/file')
def all_file():
    name = "file"
    file_db = db.session.query(ormFiles).all()
    file = []
    for row in file_db:
        file.append({"id": row.id, "name": row.name, "file_text": row.file_text, "expansion": row.expansion,
                     "versions": row.versions,
                     "created": row.created, "rating": row.rating, "project_id": row.project_id})
    return render_template('allFile.html', name=name, file=file, action="/all/file")


@app.route('/create/user', methods=['GET', 'POST'])
def create_user():
    form = CreateUser()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_user.html', form=form, form_name="New user", action="create/user")
        else:

            ids = db.session.query(ormUsers).all()
            check = True
            for row in ids:
                if row.login == form.login.data:
                    check = False

            new_var = ormUsers(

                login=form.login.data,
                password=form.password.data,
                email=form.email.data,
                lastname=form.lastname.data,
                firstname=form.firstname.data,

            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_user'))
            else:
                form.login.errors = "this user already exists"

    return render_template('create_user.html', form=form, form_name="New user", action="create/user")


@app.route('/create/reposytory', methods=['GET', 'POST'])
def create_reposytory():
    form = CreateReposytory()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_reposytory.html', form=form, form_name="New reposytory",
                                   action="create/reposytory")
        else:

            ids = db.session.query(ormUsers).all()
            check = False
            for row in ids:
                if row.id == form.user_id.data:
                    check = True

            new_var = ormReposytoty(

                name=form.name.data,
                description=form.description.data,
                countofprojects=form.countofprojects.data,
                user_id=form.user_id.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_reposytory'))

    return render_template('create_reposytory.html', form=form, form_name="New reposytory", action="create/reposytory")


@app.route('/create/project', methods=['GET', 'POST'])
def create_project():
    form = CreateProject()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_project.html', form=form, form_name="New project", action="create/project")
        else:

            ids = db.session.query(ormReposytoty).all()
            check = False
            for row in ids:
                if row.id == form.reposytoty_id.data:
                    check = True

            new_var = ormProject(

                name=form.name.data,
                description=form.description.data,
                countoffiles=form.countoffiles.data,
                reposytoty_id=form.reposytoty_id.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_project'))

    return render_template('create_project.html', form=form, form_name="New project", action="create/project")


@app.route('/create/file', methods=['GET', 'POST'])
def create_file():
    form = CreateFile()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_file.html', form=form, form_name="New file", action="create/file")
        else:

            ids = db.session.query(ormProject).all()
            check = False
            for row in ids:
                if row.id == form.project_id.data:
                    check = True

            new_var = ormFiles(

                name=form.name.data,
                file_text=form.file_text.data,
                expansion=form.expansion.data,
                versions=form.versions.data,
                rating=form.rating.data,
                project_id=form.project_id.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_file'))

    return render_template('create_file.html', form=form, form_name="New file", action="create/file")


@app.route('/delete/user', methods=['GET'])
def delete_user():
    id = request.args.get('id')

    result = db.session.query(ormUsers).filter(ormUsers.id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_user'))


@app.route('/delete/reposytory', methods=['GET'])
def delete_reposytory():
    id = request.args.get('id')

    result = db.session.query(ormReposytoty).filter(ormReposytoty.id == id).one()

    # db.session.delete(result)
    #
    # result = db.session.query(ormProject).filter(ormProject.reposytoty_id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_reposytory'))


@app.route('/delete/project', methods=['GET'])
def delete_project():
    id = request.args.get('id')

    result = db.session.query(ormProject).filter(ormProject.id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_project'))


@app.route('/delete/file', methods=['GET'])
def delete_file():
    id = request.args.get('id')

    result = db.session.query(ormFiles).filter(ormFiles.id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_file'))


@app.route('/edit/user', methods=['GET', 'POST'])
def edit_user():
    form = EditUser()
    id = request.args.get('id')
    if request.method == 'GET':

        users = db.session.query(ormUsers).filter(ormUsers.id == id).one()

        form.login.data = users.login
        form.password.data = users.password
        form.email.data = users.email
        form.lastname.data = users.lastname
        form.firstname.data = users.firstname

        return render_template('edit_user.html', form=form, form_name="Edit user",
                               action="edit/user?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_user.html', form=form, form_name="Edit user", action="edit/user?id=" + id)
        else:

            # find user
            var = db.session.query(ormUsers).filter(ormUsers.id == id).one()
            print(var)

            # update fields from form data

            var.login = form.login.data
            var.password = form.password.data
            var.email = form.email.data
            var.lastname = form.lastname.data
            var.firstname = form.firstname.data
            db.session.commit()

            return redirect(url_for('all_user'))


@app.route('/edit/reposytory', methods=['GET', 'POST'])
def edit_reposytory():
    form = EditReposytory()
    id = request.args.get('id')
    if request.method == 'GET':

        reposytory = db.session.query(ormReposytoty).filter(ormReposytoty.id == id).one()

        form.name.data = reposytory.name
        form.description.data = reposytory.description
        form.countofprojects.data = reposytory.countofprojects

        return render_template('edit_reposytory.html', form=form, form_name="Edit reposytory",
                               action="edit/reposytory?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_reposytory.html', form=form, form_name="Edit reposytory",
                                   action="edit/reposytory?id=" + id)
        else:

            # find user
            var = db.session.query(ormReposytoty).filter(ormReposytoty.id == id).one()
            print(var)

            # update fields from form data

            var.name = form.name.data
            var.description = form.description.data
            var.countofprojects = form.countofprojects.data
            db.session.commit()

            return redirect(url_for('all_reposytory'))


@app.route('/edit/project', methods=['GET', 'POST'])
def edit_project():
    form = EditProject()
    id = request.args.get('id')
    if request.method == 'GET':

        project = db.session.query(ormProject).filter(ormProject.id == id).one()

        form.name.data = project.name
        form.description.data = project.description
        form.countoffiles.data = project.countoffiles

        return render_template('edit_project.html', form=form, form_name="Edit project",
                               action="edit/project?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_project.html', form=form, form_name="Edit project", action="edit/project?id=" + id)
        else:

            # find user
            var = db.session.query(ormProject).filter(ormProject.id == id).one()
            print(var)

            # update fields from form data

            var.name = form.name.data
            var.description = form.description.data
            var.countoffiles = form.countoffiles.data
            db.session.commit()

            return redirect(url_for('all_project'))


@app.route('/edit/file', methods=['GET', 'POST'])
def edit_file():
    form = EditFile()
    id = request.args.get('id')
    if request.method == 'GET':

        file = db.session.query(ormFiles).filter(ormFiles.id == id).one()

        form.name.data = file.name
        form.file_text.data = file.file_text
        form.versions.data = file.versions
        form.rating.data = file.rating

        return render_template('edit_file.html', form=form, form_name="Edit file",
                               action="edit/file?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_file.html', form=form, form_name="Edit file", action="edit/file?id=" + id)
        else:

            # find user
            var = db.session.query(ormFiles).filter(ormFiles.id == id).one()
            print(var)

            # update fields from form data

            var.name = form.name.data
            var.file_text = form.file_text.data
            var.versions = form.versions.data
            var.rating = form.rating.data
            db.session.commit()

            return redirect(url_for('all_file'))


@app.route('/dashboard')
def dashboard():
    query1 = (
        db.session.query(
            func.count(),
            ormFiles.expansion
        ).group_by(ormFiles.expansion)
    ).all()

    query = (
        db.session.query(
            func.count(ormUsers.id),
            ormUsers.created
        ).group_by(ormUsers.created)
    ).all()

    dates, counts = zip(*query)
    bar = go.Bar(
        x=counts,
        y=dates
    )

    skills, user_count = zip(*query1)
    pie = go.Pie(
        labels=user_count,
        values=skills
    )
    print(dates, counts)
    print(skills, user_count)

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)


@app.route('/clasteresation', methods=['GET', 'POST'])
def claster():
    df = pd.DataFrame()

    for name, expansion in db.session.query(ormProject.name, ormFiles.expansion).join(ormFiles,
                                                                                      ormProject.id == ormFiles.project_id):
        print(name, expansion)
        df = df.append({"name": name, "expansion": expansion}, ignore_index=True)

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
            ormFiles.expansion
        ).group_by(ormFiles.expansion)
    ).all()
    skills, user_count = zip(*query1)
    pie = go.Pie(
        labels=user_count,
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
    for count_proj, count_files in db.session.query(ormReposytoty.countofprojects, ormProject.countoffiles).join(
            ormReposytoty,
            ormReposytoty.id == ormProject.reposytoty_id):
        print(count_proj, count_files)
        df = df.append({"count_proj": float(count_proj), "count_files": float(count_files)}, ignore_index=True)
    db.session.close()
    scaler = StandardScaler()
    scaler.fit(df[["count_proj"]])
    train_X = scaler.transform(df[["count_proj"]])
    # print(train_X, df[["count_files"]])
    reg = LinearRegression().fit(train_X, df[["count_files"]])

    test_array = [[3]]
    test = scaler.transform(test_array)
    result = reg.predict(test)

    query1 = db.session.query(ormReposytoty.countofprojects, ormProject.countoffiles).join(
            ormReposytoty, ormReposytoty.id == ormProject.reposytoty_id).all()
    count_pr, count_fl = zip(*query1)
    scatter = go.Scatter(
        x=count_pr,
        y=count_fl,
        mode = 'markers',
        marker_color='rgba(255, 0, 0, 100)',
        name = "data"
    )
    x_line = np.linspace(0, 10)
    y_line = x_line * reg.coef_[0, 0] + reg.intercept_[0]
    line = go.Scatter(
        x=x_line,
        y=y_line,
        mode = 'lines',
        marker_color='rgba(0, 0, 255, 100)',
        name = "regretion"
    )
    data = [scatter, line]
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('regretion.html', row=int(round(result[0, 0])), test_data=test_array[0][0], coef=reg.coef_[0],
                           coef1=reg.intercept_, graphsJSON = graphsJSON)

@app.route('/clasification', methods=['GET', 'POST'])
def clasification():
    df = pd.DataFrame()
    for file_text, rating in db.session.query(ormFiles.file_text, ormFiles.rating):
        print(file_text, rating)
        df = df.append({"file_name": file_text, "rating": float(rating)}, ignore_index=True)
    # db.session.close()

    df['count_symbols'] = df['file_name'].apply(len)
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
            for id, name, Expansion in db.session.query(ormFiles.id, ormFiles.name, ormFiles.expansion
                                                        ):
                if name == form.nameOfProject.data and Expansion == form.Expansion.data:
                    list_event.append(id)

            return redirect(url_for('searchList'))

    return render_template('search.html', form=form, form_name="Search", action="search")

@app.route('/search/result')
def searchList():
    res = []
    try:
        for i in list_event:
            version,rating = db.session \
                .query(ormFiles.versions, ormFiles.rating).filter(ormFiles.id == i).one()
            res.append(
                {"version": version, "rating": rating})
    except:
        print("don't data")
    print(list_event)

    return render_template('search_list_event.html', name="result", results=res, action="/search/result")
if __name__ == '__main__':
    app.run()

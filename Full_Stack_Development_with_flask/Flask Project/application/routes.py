from application import app, db, api

from flask import render_template, request, json, Response, redirect, flash, url_for, session, jsonify

# Importing data models
from application.models import User, Course, Enrollment

# Importing forms
from application.forms import LoginForm, RegistrationForm

from flask_restplus import Resource

from application.courses_aggregate_list import course_list

courseData = [{"courseID": "1111", "title": "PHP 101", "description": "Intro to PHP", "credits": 3, "term": "Fall, Spring"}, {"courseID": "2222", "title": "Java 1", "description": "Intro to Java Programming", "credits": 4, "term": "Spring"}, {"courseID": "3333", "title": "Adv PHP 201",
                                                                                                                                                                                                                                                   "description": "Advanced PHP Programming", "credits": 3, "term": "Fall"}, {"courseID": "4444", "title": "Angular 1", "description": "Intro to Angular", "credits": 3, "term": "Fall, Spring"}, {"courseID": "5555", "title": "Java 2", "description": "Advanced Java Programming", "credits": 4, "term": "Fall"}]


###################### API ######################
# Performing CRUD operations( create(post), read(get), update(put) , delete(delete))

@api.route('/api', '/api/')
class GetAndPost(Resource):

    # get all users
    def get(self):
        return jsonify(User.objects.all())

    # Adding user to database using post request
    def post(self):
        data = api.payload  # Getting data from postman
        user = User(user_id=data['user_id'], email=data['email'],
                    first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])  # Saving password after hashing
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))


@api.route('/api/<idx>')
class GetUpdateDelete(Resource):

    # get one user
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    # Updating existing user using put method
    def put(self, idx):

        # Getting updated user details entered as raw json body.
        data = api.payload
        # ** are used for packing and unpacking in python. SO it automatically unpacks the data and updates it
        User.objects(user_id=idx).update(**data)

        return jsonify(User.objects(user_id=idx))

    # deleting user using delete method
    def delete(self,idx):

        User.objects(user_id = idx).delete()

        return jsonify("User is deleted!")



##################################################


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', index=True)


@app.route('/login', methods=['GET', 'POST'])
def login():

    # Preventing logged in user from going to login route again
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()

    # Validation
    if form.validate_on_submit():
        # email = request.form['email']
        # OR
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()

        # Checking if user is registered or not and if password matched or not
        if user and user.get_password(password):
            flash(f"{user.first_name} You are successfully logged in!", "success")

            # Adding user details to session
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect(url_for('index'))
        else:
            flash("You're not registered!", "danger")
    return render_template('login.html', title="Login", form=form, login=True)


@app.route('/logout')
def logout():
    # Remove user from session

    # We can set the value of the session attribute as created in login route to False
    session['user_id'] = False

    # Instead of setting value to false, we can also pop that value.
    session.pop('username', None)

    return redirect(url_for('index'))


@app.route('/courses')
@app.route('/courses/<term>')
def courses(term=None):

    if term is None:
        term = "Spring 2020"
    # Retrieving the courses from db in increasing order of courseID, that is why we put + before courseID
    classes = Course.objects.order_by('+courseID')
    # print(courseData)
    return render_template('courses.html', courseData=classes, term=term, courses=True)


@app.route('/register', methods=['get', 'post'])
def register():
     # Preventing logged in user from going to register route again
    if session.get('username'):
        return redirect(url_for('index'))

    form = RegistrationForm()

    # Validate_on_submit will automatically call teh validate_email method in Registration_form class and check if mail already exist  or not.
    if form.validate_on_submit():
        # getting total no. of documents in user collection
        user_id = User.objects.count()

        # incrementing th user id by 1 as user id needs to be unique
        user_id += 1

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email,
                    first_name=first_name, last_name=last_name)
        user.set_password(password)  # Saving password after hashing
        user.save()
        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))

    return render_template('register.html', title="Register", form=form, register=True)


@app.route('/enrollment', methods=['GET', 'POST'])
def enrollment():

    # If not signed in, return to login page
    if not session.get('username'):
        return redirect(url_for('login'))

    data = {}
    data['courseID'] = request.form.get('courseID')
    # We can access POST form data using request.form.get('name') OR request.form['name'] ,
    data['courseTitle'] = request.form.get('title')

    # data['title'] = request.form['title']
    # but if we use [], the name (i.e. title) must be present else it will crash. Using .get('title') will do automatically do the
    # error handeling for us.
    data['term'] = request.form.get('term')

    # Setting user_id from session varable
    user_id = session.get('user_id')

    # Checking if we are coming from course page or enrollment page
    if data['courseID']:
        if Enrollment.objects(user_id=user_id, courseID=data['courseID']):
            flash(
                f"It seems that you have already enrolled in this course {data['courseTitle']}!", "danger")
            return redirect(url_for('courses'))
        else:
            Enrollment(user_id=user_id, courseID=data['courseID']).save()
            flash(
                f"Congratulations! You are enrolled in {data['courseTitle']}.", "success")
    classes = course_list(user_id)
    return render_template('enrollment.html', enrollment=True, title="Enrollment", classes=classes)


# @app.route('/api')
# @app.route('/api/<id_index>')
# def api(id_index=None):
#     if id_index == None:
#         data = courseData
#     else:
#         data = courseData[int(id_index)]
#     return Response(json.dumps(data), mimetype='application/json')


@app.route('/user')
def user():

    # User(user_id=1,first_name="Shivam",last_name="Shukla",email="shivam@uta.com",password="1234abc").save()

    users = User.objects.all()

    return render_template('user.html', users=users)

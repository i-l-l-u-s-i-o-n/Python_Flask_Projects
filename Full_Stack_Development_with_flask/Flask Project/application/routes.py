from application import app,db

from flask import render_template, request, json, Response, redirect ,flash, url_for

# Importing data models 
from application.models import User,Course,Enrollment

# Importing forms
from application.forms import LoginForm , RegistrationForm
courseData = [{"courseID": "1111", "title": "PHP 101", "description": "Intro to PHP", "credits": 3, "term": "Fall, Spring"}, {"courseID": "2222", "title": "Java 1", "description": "Intro to Java Programming", "credits": 4, "term": "Spring"}, {"courseID": "3333", "title": "Adv PHP 201",
                                                                                                                                                                                                                                                   "description": "Advanced PHP Programming", "credits": 3, "term": "Fall"}, {"courseID": "4444", "title": "Angular 1", "description": "Intro to Angular", "credits": 3, "term": "Fall, Spring"}, {"courseID": "5555", "title": "Java 2", "description": "Advanced Java Programming", "credits": 4, "term": "Fall"}]


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', index=True)


@app.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()

    # Validation
    if form.validate_on_submit():
        if request.form['email'] =='shivam@uta.com':
            flash("You are successfully logged in!","success")
            return redirect(url_for('index'))
        else:
            flash("You're not registered!","danger")
    return render_template('login.html',title="Login", form=form, login=True)


@app.route('/courses')
@app.route('/courses/<term>')
def courses(term="Spring 2020"):
    # print(courseData)
    return render_template('courses.html', courseData=courseData, term=term, courses=True)


@app.route('/register')
def register():
    return render_template('register.html', register=True)


@app.route('/enrollment', methods=['POST'])
def enrollment():
    data = {}
    data['id'] = request.form.get('courseID')
    # We can access POST form data using request.form.get('name') OR request.form['name'] ,
    data['title'] = request.form['title']
    # but if we use [], the name (i.e. title) must be present else it will crash. Using .get('title') will do automatically do the
    # error handeling for us.
    data['term'] = request.form.get('term')

    return render_template('enrollment.html', data=data)


@app.route('/api')
@app.route('/api/<id_index>')
def api(id_index=None):
    if id_index == None:
        data = courseData
    else:
        data = courseData[int(id_index)]
    return Response(json.dumps(data), mimetype='application/json')




@app.route('/user')
def user():
   
    # User(user_id=1,first_name="Shivam",last_name="Shukla",email="shivam@uta.com",password="1234abc").save()

    users = User.objects.all()

    return render_template('user.html',users=users)
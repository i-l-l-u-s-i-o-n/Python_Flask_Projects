from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/your-url', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        # If we are using get, we can use the data in the request by request.args['name']
        # return render_template('your-url.html',code=request.args['code'])

        # If we are handeling the POST request, we have to use request.form['name]
        return render_template('your-url.html', code=request.form['code'])

    else:
        # Also do return redirect('/') but using url_for, we can directly put name.
        # We can also had rendered the home page instead of redirecting but redirection also makes changes to the URL !!
        return redirect(url_for(home))

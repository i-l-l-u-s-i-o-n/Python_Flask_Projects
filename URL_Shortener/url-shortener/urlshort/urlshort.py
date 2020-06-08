from flask import render_template, request, redirect, url_for, flash,abort,session,jsonify, Blueprint
import json
import os.path
from datetime import datetime
# For securely uploading the files and prevent attacks during file upload
from werkzeug.utils import secure_filename

app = Blueprint('urlshort',__name__)


@app.route('/')
def home():
    return render_template('home.html',codes=session)


@app.route('/your-url', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':

        urls = {}

        # If file already exist, load the urls.
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        # If short name already exist in file, display flash message.
        if request.form['code'] in urls.keys():
            flash('That short name already taken.Please select another!')
            return redirect(url_for('urlshort.home'))

        # Checking if user is shortening the URL or the FILE.
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        # else file is shortened
        else:
            # Uploaded files can be accessed using request.files
            f = request.files['file']

            # The issue here is that the files which user uploads can have the same name.
            # so to overcome this issue, we can add shortname of the file the original name and the save the file.
            # But here comes another issue that user may try to attack to having special filename.
            # So to overcome this we can use secure_filename() utility to prevent these action.
            file_full_name = request.form['code'] + secure_filename(f.filename)

            # Saving the uploaded file to system
            f.save(
                '/home/shivam/GIT/Python_Flask_Projects/URL_Shortener/url-shortener/urlshort/static/user_files/' + file_full_name)
            urls[request.form['code']] = {'file': file_full_name}

        with open('urls.json', 'w') as urls_file:
            json.dump(urls, urls_file)
            
            # Storing the codes into session as keys and as values we set boolean such as True for all or we can also store timestamp and display it with keys.
            session[request.form['code']] = str(datetime.now()).split('.')[0]

        # If we are using get, we can use the data in the request by request.args['name']
        # return render_template('your-url.html',code=request.args['code'])
        # If we are handeling the POST request, we have to use request.form['name]

        return render_template('your_url.html', code=request.form['code'])

    else:
        # Also do return redirect('/') but using url_for, we can directly put name.
        # We can also had rendered the home page instead of redirecting but redirection also makes changes to the URL !!
        return redirect(url_for('urlshort.home'))


@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)

            if code in urls.keys():
                
                # checking if code is for url or file.
                if 'url' in urls[code].keys():
                    #redirecting to the original url obtained from dictionary.
                    return redirect(urls[code]['url'])

                # Else we have to render a file hat user fas uploaded.
                else:

                    return redirect(url_for('static', filename='user_files/'+urls[code]['file']))


    # Return error if no code is found.
    return abort(404)

# Handeling the returned error if no code found.
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404  # we also returning the 404 error so that in some cases broesr can help the user.



# Creating API
@app.route('/api')
def url_api():
    return jsonify(list(session.keys()))
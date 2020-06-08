from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path

# For securely uploading the files and prevent attacks during file upload
from werkzeug.utils import secure_filename


app = Flask(__name__)
# Secret key to send the data securely between different pages. It needs to be random and long
app.secret_key = 'if4398fh494cm8m9h934fr934f34f'


@app.route('/')
def home():
    return render_template('home.html')


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
            return redirect('/')

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
                '/home/shivam/GIT/Python_Flask_Projects/URL_Shortener/url-shortener' + file_full_name)
            urls[request.form['code']] = {'file': file_full_name}

        with open('urls.json', 'w') as urls_file:
            json.dump(urls, urls_file)

        # If we are using get, we can use the data in the request by request.args['name']
        # return render_template('your-url.html',code=request.args['code'])
        # If we are handeling the POST request, we have to use request.form['name]

        return render_template('your-url.html', code=request.form['code'])

    else:
        # Also do return redirect('/') but using url_for, we can directly put name.
        # We can also had rendered the home page instead of redirecting but redirection also makes changes to the URL !!
        return redirect(url_for(home))

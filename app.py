from flask import Flask, render_template, request, session, flash, redirect, send_from_directory
from flask_session import Session
import os
from werkzeug.utils import secure_filename
import generation
from socket import gethostname

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1000 * 1000  # limit file size to 4MB

# Configure the session
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.add_url_rule(
    "/uploads/<filename>", endpoint="uploads", build_only=True
)
Session(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # check if browser submitted an empty file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # check if file is allowed and save it
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            session['filename'] = filename
            
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            
            session['file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(session['file_path'])
            # Save the file information to the database
            # Generate the color palette using the selected method
            # Return the generated palette and the image to display
            flash("Image uploaded successfully!", "success")
            return render_template('index.html', filename=session['filename'], enable_generate=True)
        else:
            flash("Invalid file extension. Only jpg, jpeg, png, and gif are allowed.", "error")
            return redirect(request.url) 

    return render_template('index.html', enable_generate=False)


@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/method', methods=['GET', 'POST'])
def gen_method():
    if request.method == 'POST':
        session['gen_method'] = request.form['method']
        session['num_colors'] = request.form['number']
        selected_method = session.get('gen_method', None)
        palette_generator = generation.methods.get(selected_method, generation.kmeans_generation)
        session['palette'] = palette_generator(session['file_path'], session['num_colors'])
        return render_template('index.html', filename=session['filename'], palette=session['palette'], enable_generate=True)
    
    return render_template('index.html', filename=session['filename'])


if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run()

from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory
from flask_session import Session
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure the session
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file and file.filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Save the file information to the database
            # Generate the color palette using the selected method
            # Return the generated palette and the image to display
            flash("Image uploaded successfully!", "success")
            return render_template('index.html', filename=filename)
        else:
            flash("Invalid file extension. Only jpg, jpeg, png, and gif are allowed.", "error")     

    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

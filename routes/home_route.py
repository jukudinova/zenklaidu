from flask import Blueprint, request, render_template, redirect, url_for, current_app, flash
from werkzeug.utils import secure_filename
from services.training_data import TrainingData
from extensions import db
import pandas as pd
import os

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    return render_template("home.html")


@home_bp.route("/upload_form")
def upload_form():
    return render_template("upload_form.html")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in current_app.config["DATABASE_ALLOWED_EXTENSIONS"]
    )


@home_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file part in request.")
        return redirect(url_for("home.upload_form"))

    file = request.files["file"]

    if file.filename == "":
        flash("No selected file.")
        return redirect(url_for("home.upload_form"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath)

            required_columns = [
                "file_name", "width", "height", 
                "roi_x1", "roi_y1", "roi_x2", "roi_y2", "class_id"
            ]
            if not all(col in df.columns for col in required_columns):
                flash("CSV file is missing required columns.")
                return redirect(url_for("home.upload_form"))

            for _, row in df.iterrows():
                new_data = TrainingData(
                    file_name=row["file_name"],
                    width=row["width"],
                    height=row["height"],
                    roi_x1=row["roi_x1"],
                    roi_y1=row["roi_y1"],
                    roi_x2=row["roi_x2"],
                    roi_y2=row["roi_y2"],
                    class_id=row["class_id"],
                )
                db.session.add(new_data)

            db.session.commit()
            flash("File successfully uploaded and data added.")
            return redirect(url_for("home.home"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error processing file: {e}")
            return redirect(url_for("home.upload_form"))

    flash("Invalid file format. Only CSV files allowed.")
    return redirect(url_for("home.upload_form"))

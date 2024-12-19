from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import HealthRecord

# blueprint for routes
routes = Blueprint('routes', __name__)

@routes.route("/")
def index():
    records = HealthRecord.query.order_by(HealthRecord.id).all()
    return render_template("index.html", records=records)

@routes.route("/add", methods=["GET", "POST"])
def add_record():
    if request.method == "POST":
        new_record = HealthRecord(
            name=request.form["name"],
            age=request.form["age"],
            condition=request.form["condition"]
        )
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for("routes.index"))
    return render_template("add_record.html")

@routes.route("/edit/<int:record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    record = HealthRecord.query.get_or_404(record_id)
    if request.method == "POST":
        record.name = request.form["name"]
        record.age = request.form["age"]
        record.condition = request.form["condition"]
        db.session.commit()
        return redirect(url_for("routes.index"))
    return render_template("edit_record.html", record=record)

@routes.route("/delete/<int:record_id>", methods=["GET", "POST"])
def delete_record(record_id):
    record = HealthRecord.query.get_or_404(record_id)
    if request.method == "POST":
        db.session.delete(record)
        db.session.commit()
        return redirect(url_for("routes.index"))
    return render_template("delete_confirm.html", record=record)

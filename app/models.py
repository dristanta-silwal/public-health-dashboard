from . import db

class HealthRecord(db.Model):
    __tablename__ = "health_records"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.Text, nullable=False)

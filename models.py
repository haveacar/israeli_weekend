from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Client %r>' % self.email

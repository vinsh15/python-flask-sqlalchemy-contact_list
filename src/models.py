from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    addres = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(14), unique=True, nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "address": self.addres,
            "phone": self.phone
            # do not serialize the password, its a security breach
        }
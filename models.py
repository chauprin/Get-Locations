from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class my_points(BaseModel, db.Model):
    """Model for the my_points table"""
    __tablename__ = 'my_points'

    s_no = db.Column(db.Integer, primary_key = True)
    place = db.Column(db.String)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

class clients(BaseModel, db.Model):
    """Model for the users table"""
    __tablename__ = 'clients'

    s_no = db.Column(db.Integer, primary_key = True)
    application_name = db.Column(db.String)
    application_website = db.Column(db.String)
    client_id = db.Column(db.String)
    client_secret = db.Column(db.String) 

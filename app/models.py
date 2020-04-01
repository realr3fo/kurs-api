# app/models.py

from app import db


class KursList(db.Model):
    """This class represents the kurs table."""

    __tablename__ = 'kurslists'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    currency = db.Column(db.String(3))
    erate_jual = db.Column(db.String(20))
    erate_beli = db.Column(db.String(20))
    tt_counter_jual = db.Column(db.String(20))
    tt_counter_beli = db.Column(db.String(20))
    bank_notes_jual = db.Column(db.String(20))
    bank_notes_beli = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, currency, date):
        """initialize with name."""
        self.currency = currency
        self.date = date

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return KursList.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<KursList: {}>".format(self.name)

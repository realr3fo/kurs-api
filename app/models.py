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

    def __init__(self, currency, date, erate_jual, erate_beli, tt_counter_jual, tt_counter_beli, bank_notes_jual,
                 bank_notes_beli):
        """initialize with name."""
        self.currency = currency
        self.date = date
        self.erate_jual = erate_jual
        self.erate_beli = erate_beli
        self.tt_counter_jual = tt_counter_jual
        self.tt_counter_beli = tt_counter_beli
        self.bank_notes_jual = bank_notes_jual
        self.bank_notes_beli = bank_notes_beli

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return KursList.query.all()

    @staticmethod
    def get_by_date_and_currency(date, currency):
        return KursList.query.filter_by(date=date, currency=currency).first()

    @staticmethod
    def get_by_date(date):
        return KursList.query.filter_by(date=date).all()

    @staticmethod
    def get_by_date_range(start_date, end_date):
        return KursList.query.filter(KursList.date.between(start_date, end_date)).all()

    @staticmethod
    def get_by_date_range_and_currency(start_date, end_date, currency):
        return KursList.query.filter(KursList.date.between(start_date, end_date)).filter_by(currency=currency).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<KursList: {} {} {} {} {} {} {} {}>".format(self.currency, self.date, self.erate_jual, self.erate_beli,
                                                            self.tt_counter_jual, self.tt_counter_beli,
                                                            self.bank_notes_jual, self.bank_notes_beli)

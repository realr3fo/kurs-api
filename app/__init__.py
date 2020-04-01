# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config
from flask import request, jsonify, abort

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import KursList
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/kurs', methods=['POST', 'PUT', 'GET'])
    def kurslists():
        if request.method == "POST":
            currency = str(request.data.get('currency', ''))
            date = str(request.data.get('date', ''))
            erate_jual = str(request.data.get('erate_jual', ''))
            erate_beli = str(request.data.get('erate_beli', ''))
            tt_counter_jual = str(request.data.get('tt_counter_jual', ''))
            tt_counter_beli = str(request.data.get('tt_counter_beli', ''))
            bank_notes_jual = str(request.data.get('bank_notes_jual', ''))
            bank_notes_beli = str(request.data.get('bank_notes_beli', ''))
            if currency:
                kurslist = KursList(currency=currency, date=date, erate_jual=erate_jual, erate_beli=erate_beli,
                                    tt_counter_jual=tt_counter_jual, tt_counter_beli=tt_counter_beli,
                                    bank_notes_jual=bank_notes_jual, bank_notes_beli=bank_notes_beli)
                kurslist.save()
                response = jsonify({
                    'id': kurslist.id,
                    'currency': kurslist.currency,
                    'date': kurslist.date,
                    'erate_jual': kurslist.erate_jual,
                    'erate_beli': kurslist.erate_beli,
                    'tt_counter_jual': kurslist.tt_counter_jual,
                    'tt_counter_beli': kurslist.tt_counter_beli,
                    'bank_notes_jual': kurslist.bank_notes_jual,
                    'bank_notes_beli': kurslist.bank_notes_beli,
                    'date_created': kurslist.date_created,
                    'date_modified': kurslist.date_modified
                })
                response.status_code = 201
                return response
        elif request.method == "PUT":
            currency = str(request.data.get('currency', ''))
            date = str(request.data.get('date', ''))
            erate_jual = str(request.data.get('erate_jual', ''))
            erate_beli = str(request.data.get('erate_beli', ''))
            tt_counter_jual = str(request.data.get('tt_counter_jual', ''))
            tt_counter_beli = str(request.data.get('tt_counter_beli', ''))
            bank_notes_jual = str(request.data.get('bank_notes_jual', ''))
            bank_notes_beli = str(request.data.get('bank_notes_beli', ''))
            kurslist = KursList.get_by_date_and_currency(date, currency)
            if kurslist == None:
                response = jsonify({})
                response.status_code = 404
                return response
            else:
                kurslist.currency = currency
                kurslist.date = date
                kurslist.erate_jual = erate_jual
                kurslist.erate_beli = erate_beli
                kurslist.tt_counter_jual = tt_counter_jual
                kurslist.tt_counter_beli = tt_counter_beli
                kurslist.bank_notes_jual = bank_notes_jual
                kurslist.bank_notes_beli = bank_notes_beli
                kurslist.save()
                response = jsonify({'id': kurslist.id,
                                    'currency': kurslist.currency,
                                    'date': kurslist.date,
                                    'erate_jual': kurslist.erate_jual,
                                    'erate_beli': kurslist.erate_beli,
                                    'tt_counter_jual': kurslist.tt_counter_jual,
                                    'tt_counter_beli': kurslist.tt_counter_beli,
                                    'bank_notes_jual': kurslist.bank_notes_jual,
                                    'bank_notes_beli': kurslist.bank_notes_beli,
                                    'date_created': kurslist.date_created,
                                    'date_modified': kurslist.date_modified})
                response.status_code = 200
            return response
        else:
            response = jsonify({})
            response.status_code = 404
            return response

    @app.route('/api/kurs/<string:date>', methods=['DELETE'])
    def kurslists_delete(date):
        kurslist_arr = KursList.get_by_date(date)
        print(kurslist_arr, len(kurslist_arr))
        if len(kurslist_arr) == 0:
            print("hello world")
            response = jsonify({})
            response.status_code = 404
            return
        for kurslist in kurslist_arr:
            print("dbebug here")
            kurslist.delete()
        response = jsonify({"message": "kurslists deleted successfully"})
        response.status_code = 200
        return response

    @app.route('/api/kurs/<string:currency>', methods=['GET'])
    def kurslists_get(currency):
        response = jsonify({})
        response.status_code = 404
        return response

    @app.route('/api/inidexing', methods=['GET'])
    def kurslist_indexing():
        response = jsonify({})
        response.status_code = 404
        return response

    return app

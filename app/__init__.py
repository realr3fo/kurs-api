# app/__init__.py


from datetime import date

import requests
from bs4 import BeautifulSoup

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
            start_date = request.args.get('startdate')
            end_date = request.args.get('enddate')
            kurslist_arr = KursList.get_by_date_range(start_date, end_date)
            result = []
            for kurslist in kurslist_arr:
                kurslist_obj = {'id': kurslist.id,
                                'currency': kurslist.currency,
                                'date': kurslist.date,
                                'erate_jual': kurslist.erate_jual,
                                'erate_beli': kurslist.erate_beli,
                                'tt_counter_jual': kurslist.tt_counter_jual,
                                'tt_counter_beli': kurslist.tt_counter_beli,
                                'bank_notes_jual': kurslist.bank_notes_jual,
                                'bank_notes_beli': kurslist.bank_notes_beli,
                                'date_created': kurslist.date_created,
                                'date_modified': kurslist.date_modified}
                result.append(kurslist_obj)
            response = jsonify({"data": result})
            response.status_code = 200
            return response

    @app.route('/api/kurs/<string:date>', methods=['DELETE'])
    def kurslists_delete(date):
        kurslist_arr = KursList.get_by_date(date)
        if len(kurslist_arr) == 0:
            response = jsonify({})
            response.status_code = 404
            return
        for kurslist in kurslist_arr:
            kurslist.delete()
        response = jsonify({"message": "kurslists deleted successfully"})
        response.status_code = 200
        return response

    @app.route('/api/kurs/<string:currency>', methods=['GET'])
    def kurslists_get(currency):
        start_date = request.args.get('startdate')
        end_date = request.args.get('enddate')
        kurslist_arr = KursList.get_by_date_range_and_currency(start_date, end_date, currency)
        result = []
        for kurslist in kurslist_arr:
            kurslist_obj = {'id': kurslist.id,
                            'currency': kurslist.currency,
                            'date': kurslist.date,
                            'erate_jual': kurslist.erate_jual,
                            'erate_beli': kurslist.erate_beli,
                            'tt_counter_jual': kurslist.tt_counter_jual,
                            'tt_counter_beli': kurslist.tt_counter_beli,
                            'bank_notes_jual': kurslist.bank_notes_jual,
                            'bank_notes_beli': kurslist.bank_notes_beli,
                            'date_created': kurslist.date_created,
                            'date_modified': kurslist.date_modified}
            result.append(kurslist_obj)
        response = jsonify({"data": result})
        response.status_code = 200
        return response

    @app.route('/api/indexing', methods=['GET'])
    def kurslist_indexing():

        today = date.today()

        url = 'https://www.bca.co.id/id/Individu/Sarana/Kurs-dan-Suku-Bunga/Kurs-dan-Kalkulator'

        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'html.parser')
        rows = soup.select('tbody tr')
        counter = 0
        result = []
        for elem in rows:
            each_currency = elem.select('td')
            currency_symbol = each_currency[0].text
            erate_beli = each_currency[1].text
            erate_jual = each_currency[2].text
            tt_counter_beli = each_currency[3].text
            tt_counter_jual = each_currency[4].text
            bank_notes_beli = each_currency[5].text
            bank_notes_jual = each_currency[6].text

            kurslist = KursList(currency=currency_symbol, date=today, erate_jual=erate_jual, erate_beli=erate_beli,
                                tt_counter_jual=tt_counter_jual, tt_counter_beli=tt_counter_beli,
                                bank_notes_jual=bank_notes_jual, bank_notes_beli=bank_notes_beli)
            kurslist.save()
            single_kurs_objj = {
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
            }
            result.append(single_kurs_objj)
            counter += 1
            if counter == 16:
                break
        response = jsonify({"data": result})
        response.status_code = 200
        return response

    return app

# test_kurs_api.py
import unittest
import os
import json
from datetime import date
from time import strptime

from app import create_app, db


class KursAPITestCase(unittest.TestCase):
    """This class represents the kursAPI test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        today = date.today()

        self.currency = 'IDR'
        self.date = today.strftime("%a, %d %b %Y %H:%M:%S")
        self.erate_jual = '16.440,00'
        self.erate_beli = '16.590,00'
        self.tt_counter_jual = '16.275,00'
        self.tt_counter_beli = '16.775,00'
        self.bank_notes_jual = '16.250,00'
        self.bank_notes_beli = '16.750,00'
        self.kurslist = {'currency': self.currency, 'date': self.date, 'erate_jual': self.erate_jual,
                         'erate_beli': self.erate_beli, 'tt_counter_jual': self.tt_counter_jual,
                         'tt_counter_beli': self.tt_counter_beli, 'bank_notes_jual': self.bank_notes_jual,
                         'bank_notes_beli': self.bank_notes_beli}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_kurslist_creation(self):
        """Test API can create a kurslist (POST request)"""
        res = self.client().post('/api/kurs', data=self.kurslist)
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.currency, str(res.data))
        self.assertIn(self.date, str(res.data))
        self.assertIn(self.erate_jual, str(res.data))
        self.assertIn(self.erate_beli, str(res.data))
        self.assertIn(self.tt_counter_jual, str(res.data))
        self.assertIn(self.tt_counter_beli, str(res.data))
        self.assertIn(self.bank_notes_jual, str(res.data))
        self.assertIn(self.bank_notes_beli, str(res.data))

    def test_kurslist_can_be_edited(self):
        """Test API can edit an existing kurslist. (PUT request)"""
        rv = self.client().post('/api/kurs', data=self.kurslist)
        self.assertEqual(rv.status_code, 201)
        updated_num = 123
        new_data = {'currency': 'IDR', 'date': self.date, 'erate_jual': updated_num,
                    'erate_beli': updated_num, 'tt_counter_jual': updated_num,
                    'tt_counter_beli': updated_num, 'bank_notes_jual': updated_num,
                    'bank_notes_beli': updated_num}
        res = self.client().put(
            '/api/kurs',
            data=new_data)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.currency, str(res.data))
        self.assertIn(self.date, str(res.data))
        self.assertIn(str(updated_num), str(res.data))

    def test_api_can_get_kurslists_by_date_range(self):
        """Test API can get a kurslist (GET request)."""
        res = self.client().post('/api/kurs', data=self.kurslist)
        self.assertEqual(res.status_code, 201)
        get_url = '/api/kurs?startdate=2020-01-01&enddate=%s' % self.date
        res = self.client().get(get_url)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.currency, str(res.data))
        self.assertIn(self.date, str(res.data))
        self.assertIn(self.erate_jual, str(res.data))
        self.assertIn(self.erate_beli, str(res.data))
        self.assertIn(self.tt_counter_jual, str(res.data))
        self.assertIn(self.tt_counter_beli, str(res.data))
        self.assertIn(self.bank_notes_jual, str(res.data))
        self.assertIn(self.bank_notes_beli, str(res.data))

    def test_api_can_get_kurslists_by_date_range_and_symbol(self):
        """Test API can get a kurslist (GET request)."""
        res = self.client().post('/api/kurs', data=self.kurslist)
        self.assertEqual(res.status_code, 201)
        get_url = '/api/kurs/IDR?startdate=2020-01-01&enddate=%s' % self.date
        res = self.client().get(get_url)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.currency, str(res.data))
        self.assertIn(self.date, str(res.data))
        self.assertIn(self.erate_jual, str(res.data))
        self.assertIn(self.erate_beli, str(res.data))
        self.assertIn(self.tt_counter_jual, str(res.data))
        self.assertIn(self.tt_counter_beli, str(res.data))
        self.assertIn(self.bank_notes_jual, str(res.data))
        self.assertIn(self.bank_notes_beli, str(res.data))

    def test_kurslist_indexing(self):
        """Test API can index the kurslist. (GET request)."""
        get_url = '/api/indexing'
        result = self.client().get(get_url)
        self.assertEqual(result.status_code, 200)
        self.assertIn("USD", str(result.data))
        self.assertIn("SGD", str(result.data))
        self.assertIn("MYR", str(result.data))
        self.assertIn("THB", str(result.data))

    def test_kurslist_deletion(self):
        """Test API can delete an existing kurslist. (DELETE request)."""
        rv = self.client().post('/api/kurs', data=self.kurslist)
        self.assertEqual(rv.status_code, 201)
        delete_url = '/api/kurs/%s' % self.date
        res = self.client().delete(delete_url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("kurslists deleted successfully", str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

import unittest
import web_report_app

class TestWebReport(unittest.TestCase):

    def setUp(self):
        web_report_app.app.config['TESTING'] = True
        self.app = web_report_app.app.test_client()

    def test_report(self):
        response = self.app.get('/report', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_drivers_first(self):
        response = self.app.get('/report/drivers/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_drivers_second(self):
        """if url is not exist - 404"""
        response = self.app.get('/report/driver', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_drivers_id_first(self):
        response = self.app.get('/report/drivers/?driver_id=DRR', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_drivers_id_second(self):
        """if driver_id isn't correct """
        response = self.app.get('/report/drivers/?driver_id=111', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_drivers_order(self):
        response = self.app.get('/report/drivers/?order=desc', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_drivers_data_first(self):
        response = self.app.get('/report/drivers/?driver_id=SVF', follow_redirects=True)
        self.assertEqual(response.data, b'Sebastian Vettel | FERRARI | 0:01:04.415000')

    def test_drivers_data_second(self):
        """if driver_id isn't correct """
        response = self.app.get('/report/drivers/?driver_id=111', follow_redirects=True)
        self.assertEqual(response.data, b'Driver_id is not correct. Please, try again')

if __name__ == '__main__':
    unittest.main()

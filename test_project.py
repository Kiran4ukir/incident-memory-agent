import unittest
from datetime import datetime
import app
import agent
import memory
from seed_data import INCIDENTS, DEMO_ALERT

class TestProjectComponents(unittest.TestCase):
    def test_seed_data_structure(self):
        self.assertGreater(len(INCIDENTS), 0)
        for inc in INCIDENTS:
            self.assertIn("id", inc)
            self.assertIn("service", inc)
            self.assertIn("title", inc)
            self.assertIn("symptoms", inc)
            self.assertIn("root_cause", inc)
            self.assertIn("resolution", inc)
            self.assertIsInstance(inc["date"], datetime)

    def test_incident_to_text(self):
        sample_inc = INCIDENTS[0]
        text = memory.incident_to_text(sample_inc)
        self.assertIn(sample_inc["id"], text)
        self.assertIn(sample_inc["service"], text)
        self.assertIn(sample_inc["title"], text)

    def test_app_routes_exist(self):
        with app.app.test_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 200)

            res_demo = client.get('/api/demo-alert')
            self.assertEqual(res_demo.status_code, 200)
            data = res_demo.get_json()
            self.assertIn('alert', data)
            self.assertEqual(data['alert'], DEMO_ALERT)

            res_triage_err = client.post('/api/triage', json={})
            self.assertEqual(res_triage_err.status_code, 400)

            res_resolve_err = client.post('/api/resolve', json={})
            self.assertEqual(res_resolve_err.status_code, 400)

if __name__ == '__main__':
    unittest.main()

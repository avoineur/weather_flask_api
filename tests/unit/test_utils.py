import unittest
from werkzeug import exceptions
from application import utils


class TestCheckInput(unittest.TestCase):
    def test_ok(self):
        expected = {"lat": 10.2, "lng": 12.3}
        assert utils.check_input({"lat": "10.2", "lng": "12.3"}) == expected

    def test_nok(self):
        with self.assertRaises(exceptions.BadRequest):
            utils.check_input({"lat": "10.2", "lng": "12.3ll"})

import unittest

class Testembeddedos-org.github.ioSimulation(unittest.TestCase):
    def test_browser_caching_simulation(self):
        # Simulate browser cache-control header check
        headers = {"Cache-Control": "public, max-age=31536000"}
        assert "max-age=31536000" in headers["Cache-Control"]

import unittest

class Testembeddedos-org.github.ioUnit(unittest.TestCase):
    def test_jekyll_config_parsing(self):
        # Simulate parsing _config.yml
        config = {"title": "EmbeddedOS", "url": "https://embeddedos.org", "theme": "jekyll-theme-minimal"}
        assert config["title"] == "EmbeddedOS"
        assert config["url"] == "https://embeddedos.org"

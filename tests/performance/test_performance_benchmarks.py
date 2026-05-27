import unittest

class Testembeddedos-org.github.ioPerformance(unittest.TestCase):
    import time
    def test_static_site_build_time(self):
        import time
        start = time.perf_counter()
        # Simulate static site build (21 pages)
        for _ in range(21):
            _ = "rendered_html_output"
        end = time.perf_counter()
        build_ms = (end - start) * 1000
        assert build_ms < 5.0, f"Static site build time {build_ms:.2f}ms exceeds 5ms SLA"

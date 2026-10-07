import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from negotiate import core


class NegotiateTest(unittest.TestCase):
    def test_exact_match(self):
        self.assertEqual(core.choose("text/html", ["text/html"], core.Counter()), "text/html")

    def test_no_match(self):
        self.assertEqual(core.choose("text/html", ["application/json"], core.Counter()), "")

    def test_server_order_fallback(self):
        got = core.choose("text/html, application/json",
                          ["application/json", "text/html"], core.Counter())
        self.assertEqual(got, "application/json")

    def test_empty_accept(self):
        self.assertEqual(core.choose("", ["text/html"], core.Counter()), "")

    def test_empty_server(self):
        self.assertEqual(core.choose("text/html", [], core.Counter()), "")

    def test_counter_counts(self):
        counter = core.Counter()
        core.choose("text/html", ["text/html"], counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()

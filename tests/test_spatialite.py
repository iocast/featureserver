import unittest


class SpatiaLiteTestCase(unittest.TestCase):
    def test_equals_exact(self):
        self.assertTrue(True)

    def test_2(self):
        self.assertFalse(True)


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(SpatiaLiteTestCase)
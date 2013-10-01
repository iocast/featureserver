import os
import unittest


class BaseTest(unittest.TestCase):
    
    def read_file(self, filename):
        """
            Process a file stored in tests/data/ and return its content.
            """
        current_path = os.path.dirname(os.path.realpath(__file__))
        fixture_path = os.path.join(
                                    current_path,
                                    'data',
                                    filename
                                    )
        f = open(fixture_path)
        return f.read()

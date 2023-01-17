import unittest
from utils.regular_expression import check_re


class TestCheckRe(unittest.TestCase):
    def test_valid_input(self):
        self.assertTrue(check_re("12/12/2022"))
        self.assertTrue(check_re("  12/12/2022  "))
        self.assertTrue(check_re("01/01/2022"))
        self.assertTrue(check_re("31/12/2022"))

    def test_invalid_input(self):
        self.assertFalse(check_re(""))
        self.assertFalse(check_re("12/12/202"))
        self.assertFalse(check_re("12/12/20224"))
        self.assertFalse(check_re("12/12/22"))
        self.assertFalse(check_re("12/12/20220"))
        self.assertFalse(check_re("32/12/2022"))
        self.assertFalse(check_re("12/13/2022"))
        self.assertFalse(check_re("12/12/202a"))
        self.assertFalse(check_re("12/12/202 2"))

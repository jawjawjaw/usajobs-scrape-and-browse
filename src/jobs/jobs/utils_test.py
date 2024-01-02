import unittest

from jobs.utils import strip_date


class TestUtils(unittest.TestCase):
    def test_strip_date(self):
        # Test case 1: Valid date with milliseconds
        date1 = "2022-01-01T12:34:56.789Z"
        expected1 = "2022-01-01T12:34:56"
        self.assertEqual(strip_date(date1), expected1)

        # Test case 2: Valid date without milliseconds
        date2 = "2022-01-01T12:34:56Z"
        expected2 = "2022-01-01T12:34:56Z"
        self.assertEqual(strip_date(date2), expected2)

        # Test case 3: Empty string
        date3 = ""
        expected3 = ""
        self.assertEqual(strip_date(date3), expected3)

        # Test case 4: Date with no time component
        date4 = "2022-01-01"
        expected4 = "2022-01-01"
        self.assertEqual(strip_date(date4), expected4)

        # Test case 5: Date with only milliseconds
        date5 = ".123Z"
        expected5 = ""
        self.assertEqual(strip_date(date5), expected5)


if __name__ == "__main__":
    unittest.main()

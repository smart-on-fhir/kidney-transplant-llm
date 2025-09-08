import unittest
from datetime import datetime
from transplant_llm import parse_dates

class TestDates(unittest.TestCase):

    def test_simple(self):
        text = '2020-09-28'
        expected = datetime(2020, 9, 28)
        actual = parse_dates.parse_date(text)
        print(actual)
        self.assertEqual(expected, actual)

    def test_parse_dates(self):
        self.assert_date(' 2095-03-28', 28, 3, 2095)
        self.assert_date('Nov 2093', 1, 11, 2093)
        self.assert_date('3/27', 27, 3, 9999)
        self.assert_date('04-Jul-2018', 4, 7, 2018)
        self.assert_date(' 9/17/64', 17, 9, 1964)
        self.assert_date('1/26/1910', 26, 1, 1910)
        self.assert_date('21 Jan 2013', 21, 1, 2013)
        self.assert_date('March 14, 2018', 14, 3, 2018)
        self.assert_date('03/14/2016', 14, 3, 2016)
        self.assert_date('2/13/15', 13, 2, 2015)
        self.assert_date('24 Feb 2014', 24, 2, 2014)
        self.assert_date('2/16/1953', 16, 2, 1953)
        self.assert_date('December 2015', 1, 12, 2015)
        self.assert_date('Jan 21,2020', 21, 1, 2020)
        self.assert_date('12 FEB2020',  12, 2, 2020)
        self.assert_date('12FEB2020', 12, 2, 2020)
        self.assert_date('FEB2012', 1,  2, 2012)

    def assert_date(self, text, day, month, year):
        result = parse_dates.parse_date(text)
        output_day = result.day
        output_month = result.month
        output_year = result.year
        if year is None:
            year = 9999
        if day is None:
            day = 1
        self.assertEqual(day, output_day)
        self.assertEqual(month, output_month)
        self.assertEqual(year, output_year)

if __name__ == '__main__':
    unittest.main()

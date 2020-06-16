import unittest
from Utils.Utils import filter_non_unique_individuals, BirthDateKeyedIndividual


class UtilTest(unittest.TestCase):
    _input = []

    def setUp(self):
        self._input = [
            {
                "INDI": "I1",
                "NAME": "Bob /Bob/",
                "BIRT": [1, 1, 2000]
            },
            {
                "INDI": "I2",
                "NAME": "Bob /Bob/",
                "BIRT": [1, 1, 2001]
            },
            {
                "INDI": "I3",
                "NAME": "Bob /Bob/",
                "BIRT": [1, 2, 2000]
            },
            {
                "INDI": "I4",
                "NAME": "Bob /Bob/",
                "BIRT": [2, 1, 2000]
            },
            {
                "INDI": "I5",
                "NAME": "Bob /Bob/",
                "BIRT": [3, 4, 2002]
            }
        ]

    def tearDown(self):
        self._input = None

    def test_filtering_non_uniques_on_non_unique_input(self):
        self._input.append({
            "INDI": "I90",
            "NAME": "Bob /Bob/",
            "BIRT": [1, 1, 2000]
        })
        self._input.append({
            "INDI": "I91",
            "NAME": "Bob /Bob/",
            "BIRT": [1, 1, 2001]
        })

        non_uniques = filter_non_unique_individuals(self._input)
        self.assertEqual(2, len(non_uniques.values()), "Did not return correct amount of conflicts")
        duplicate_two_thousand = non_uniques["[1, 1, 2000]Bob /Bob/"]
        self.assertEqual(2, len(duplicate_two_thousand), "Incorrect amount of conflicts for 2000 conflicts")

        expected_two_thousand = [BirthDateKeyedIndividual([1, 1, 2000], "Bob /Bob/", "I1"),
                                 BirthDateKeyedIndividual([1, 1, 2000], "Bob /Bob/", "I90")]

        self.assertListEqual(expected_two_thousand, duplicate_two_thousand, "Found entries did not match for 2000")
        duplicate_two_thousand_one = non_uniques["[1, 1, 2001]Bob /Bob/"]
        self.assertEqual(2, len(duplicate_two_thousand_one), "Incorrect amount of conflicts for 2001 conflicts")

        expected_two_thousand_one = [BirthDateKeyedIndividual([1, 1, 2001], "Bob /Bob/", "I2"),
                                     BirthDateKeyedIndividual([1, 1, 2001], "Bob /Bob/", "I91")]
        self.assertListEqual(expected_two_thousand_one, duplicate_two_thousand_one,
                             "Found entries did not match for 2001")

    def test_filtering_non_uniques_on_unique_input(self):
        non_uniques = filter_non_unique_individuals(self._input)
        self.assertEqual(len(non_uniques.values()), 0, "Dictionary is not empty")

    def test_filtering_non_uniques_on_malformed_key_input_raises(self):
        self._input.append({
            "IND": "I90",
            "NAME": "Bob /Bob/",
            "BIRT": [1, 1, 2000]
        })
        with self.assertRaises(KeyError):
            filter_non_unique_individuals(self._input)

        self._input.pop()
        self._input.append({
            "INDI": "I90",
            "NAM": "Bob /Bob/",
            "BIRT": [1, 1, 2000]
        })
        with self.assertRaises(KeyError):
            filter_non_unique_individuals(self._input)

        self._input.pop()
        self._input.append({
            "INDI": "I90",
            "NAME": "Bob /Bob/",
            "BIR": [1, 1, 2000]
        })
        with self.assertRaises(KeyError):
            filter_non_unique_individuals(self._input)


if __name__ == '__main__':
    unittest.main()

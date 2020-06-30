import unittest
from db.db_interface import GenComDb

# Ideally the backing db would be mocked with an in-memory document store, however correctly mocking MongoDB is a
# decently heavy weight process, which per the requirements does not seem needed.
class DBInterfaceTest(unittest.TestCase):

    _test_db = None

    def setUp(self) -> None:
        self._test_db = GenComDb(GenComDb.MONGO_INDIVIDUALS)
        self._test_db.dropCollection()

    def tearDown(self) -> None:
        self._test_db.dropCollection()
        self._test_db = None

    def test_get_dead_as_list(self):
        self._test_db.seed_data()
        expected_list = [{
                'INDI': 'I3',
                'NAME': 'DeDe /Pritchett/',
                'SEX': 'F',
                'BIRT': '23 JAN 1947',
                'DEAT': '31 OCT 2018',
                'FAMS': ['F2']
             }]
        dead_members = self._test_db.getDeadAsList()
        self.assertEqual(type(dead_members), type(expected_list), "Database did not return a list")
        self.assertListEqual(expected_list, dead_members, "Content of list was wrong")

    def test_no_dead_return_empty_list(self):
        self. _test_db.AddObj({
            'INDI': 'I1',
            'NAME': 'Jay /Pritchett/',
            'SEX': 'M',
            'BIRT': '23 MAY 1947',
            'FAMS': ['F1', 'F2']
        })
        self._test_db.AddObj({
            'INDI': 'I2',
            'NAME': 'Gloria /Pritchett/',
            'SEX': 'F',
            'BIRT': '10 MAY 1971',
            'FAMS': ['F1', 'F3']
        })
        expected_list = []
        dead_members = self._test_db.getDeadAsList()
        self.assertEqual(type(dead_members), type(expected_list), "Database did not return a list")
        self.assertListEqual(expected_list, dead_members, "Content of list was wrong")


if __name__ == '__main__':
    unittest.main()

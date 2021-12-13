import unittest
from sql_lib.postgresql import database

class TestDB(unittest.TestCase):

	def setUp(self) -> None:
		self.db = database(r"sql_lib\test_db.db")

	def test_getUserServicePassword(self):
		self.assertEqual(self.db.getUserServicePassword("281048238", "Test"), [('gJ_4yOf*SpT3',)])

	def test_doesUserExist(self):
		self.assertTrue(self.db.doesUserExist('281048231'))


if __name__ == "__main__":
  unittest.main()
import unittest
from phonenumberextractor import PhoneNumberExtractor

class TestPhoneNumbersExtraction(unittest.TestCase):
	
	def setUp(self):
		self.extractor = PhoneNumberExtractor()

		self.test_dict = {}
		self.test_dict['https://www.infobip.com/en/contact'] = [
			"+16 04 566 9031",
			"+551139001300",
			"+54 11 4890 8619",
			"+44 20 7837 4180",
			"+7 495 642 7243",
			"+971 52 985 1461",
			"+60 3 8601 0105",
			"+86 1500 1300 206"
		]
		self.test_dict['http://dnb.com.au/'] = [
			"13 23 33"
		]
		self.test_dict['http://dnb.com.au/contact-us.html'] = [
			"13 23 33"
		]
		self.test_dict['https://www.cialdnb.com/pt-br'] = [
			"+1 (954) 507 1116"	
		]
		self.test_dict['https://www.powerlinx.com/contact/'] = [
			"+1 (212) 465 9555"
		]
		self.test_dict['https://www.avea.com.au/'] = [
			"1800 999 977"
		]
		self.test_dict['https://www.cmsenergy.com/contact-us/default.aspx'] = [
			"(517) 788 0550",
			"(517) 768 3376",
			"(800) 390 1220",
			"(517) 788 6538",
			"(517) 788 2395",
			"(517) 788 2394"
		]
		self.test_dict['https://www.phosagro.com/contacts/'] = [
			"+7 (495) 232 96 89",
			"+7 (495) 956 19 02",
			"+7 (495) 231 31 15",
			"+ 7 (929) 600 46 42",
			"+7 (495) 956 09 64",
			"(375 17) 392 56 48",
			"(38 044) 537 04 40",
			"+41417470370",
			"+ 48 22 630 60 90",
			"+49 40 999 99 3013",
			"+ 357 25 247 797",
			"+ 33 78 38 78 078",
			"+ 381 11 430 0060",
			"+ 381 61 185 6217",
			"+ 65 6697 4560",
			"+65 6884 9451",
			"+55 11 4280 6900"
		]


	def test_1(self):
		phone_nums = self.extractor.extract_phone_numbers('https://www.infobip.com/en/contact')
		self.assertCountEqual(phone_nums, self.test_dict['https://www.infobip.com/en/contact'])

	def test_2(self):
		phone_nums = self.extractor.extract_phone_numbers('http://dnb.com.au/')
		self.assertCountEqual(phone_nums, self.test_dict['http://dnb.com.au/'])

	def test_3(self):
		phone_nums = self.extractor.extract_phone_numbers('http://dnb.com.au/contact-us.html')
		self.assertCountEqual(phone_nums, self.test_dict['http://dnb.com.au/contact-us.html'])

	def test_4(self):
		phone_nums = self.extractor.extract_phone_numbers('https://www.cialdnb.com/pt-br')
		self.assertCountEqual(phone_nums, self.test_dict['https://www.cialdnb.com/pt-br'])

	def test_5(self):
		phone_nums = self.extractor.extract_phone_numbers('https://www.powerlinx.com/contact/')
		self.assertCountEqual(phone_nums, self.test_dict['https://www.powerlinx.com/contact/'])

	def test_6(self):
		phone_nums = self.extractor.extract_phone_numbers('https://www.avea.com.au/')
		self.assertCountEqual(phone_nums, self.test_dict['https://www.avea.com.au/'])

	def test_7(self):
		phone_nums = self.extractor.extract_phone_numbers('https://www.cmsenergy.com/contact-us/default.aspx')
		self.assertCountEqual(phone_nums, self.test_dict['https://www.cmsenergy.com/contact-us/default.aspx'])

	def test_8(self):
		phone_nums = self.extractor.extract_phone_numbers('https://www.phosagro.com/contacts/')
		self.assertCountEqual(phone_nums, self.test_dict['https://www.phosagro.com/contacts/'])


if __name__ == "__main__":
	unittest.main()
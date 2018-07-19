import sys
from phonenumberextractor import PhoneNumberExtractor

def print_result(phone_nums):
	result = ', '.join(phone_nums)
	print (result)

if __name__ == "__main__":
	url = sys.argv[1]	
	extractor = PhoneNumberExtractor()
	matches = extractor.extract_phone_numbers(url)
	print_result(matches)


import urllib
import urllib.request
import re
import threading
import time
import sys
from bs4 import BeautifulSoup, Comment
from urllib.error import URLError, HTTPError


class PhoneNumberExtractor:
	"""
	PhoneNumberExtractor extracts phone numbers from given website url
	"""

	def __init__(self):
		"""
		Attributes:
			pattern_*_*: Different regex patterns for extracting phone numbers
			clean_phonenum_pattern: Specified clean format for phone number
		"""
		self.pattern_0_a = re.compile(r'\+[-()\s\d]+?(?=\s*[+<,\.;])')
		self.pattern_0_b = re.compile(r'\(\d[-()\s\d]+?(?=\s*[+<,\.;])')
		self.pattern_1_a = re.compile(r'\d+(?: \d+){2,}')
		self.pattern_1_b = re.compile(r'\(\d+\)(?: \d+){2,}')

		self.clean_phonenum_pattern = re.compile('[^0-9\+()]')


	def _remove_attrs(self, soup):
		"""Method which removes unnecessary attributes from html elements
		Args:
			soup - BeautifulSoup object which represents html document
		Returns:
			BeautifulSoup object without attributes in html elements
		"""
		for tag in soup.findAll(True): 
			tag.attrs = {}
		return soup


	def _contains_digit(self, text):
		return any(c.isdigit() for c in text)


	def _remove_duplicates(self, matches):
		"""Method which removes duplicates or very similar numbers 
		(result of using different regexes) from list of phone numbers

		Args:
			matches - list of matched phone numbers
		Returns:
			List of phone numbers but without duplicates
		"""
		num_chars_to_check = 6
		unique_matches = []
		i = 0
		while i < len(matches):
			is_duplicate = False
			j = 0
			while j < len(matches):
				if i == j:
					j += 1
					continue
				if matches[i][-num_chars_to_check:] == matches[j][-num_chars_to_check:]:
					if len(matches[i]) < len(matches[j]):
						is_duplicate = True
						break
				j += 1
			if not is_duplicate:
				unique_matches.append(matches[i])
			i += 1
		return set(unique_matches)


	def _match_pattern(self, pattern, text):
		"""Method which uses regex to find matching phone numbers from text
		Args:
			pattern - regex pattern that is used for finding phone number
			text - string which is searched for phone numbers
		Returns: 
			list of matching phone numbers
		"""
		all_matched = re.findall(pattern, text)
		for matchedtext in all_matched:
			if self._contains_digit(matchedtext):
				matches.append(matchedtext.strip())


	def _find_matches(self, text, pttrns):
		"""Method which combines different regexes to find phone numbers in text
		Args:
			text - string which is searched for phone numbers
			pttrns - list of regex patterns used for searching
		Returns:
			list of matching phone numbers
		"""
		global matches
		matches = []
		#threads = []

		start = time.time()
		for pattern in pttrns:
			self._match_pattern(pattern, text)
		#	pattern_thread = threading.Thread(target=self._match_pattern, args=(pattern, text))
		#	threads.append(pattern_thread)
		#	pattern_thread.start()

		#for t in threads:
		#	t.join()
		end = time.time()
			
		return self._remove_duplicates(matches)


	def _retrieve_html_from_url(self, url):
		"""Method which connects to website url, and retrieves html document as string
		Args:
			url - website url
		Returns:
			String representation of html document
		"""
		req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
		try:
			con = urllib.request.urlopen( req )
		except HTTPError as e:
			sys.stderr.write("HTTPError: " + str(e.code) + "\n")
			sys.exit()
		except URLError as e:
			sys.stderr.write("URLError: " + str(e.reason) + "\n")
			sys.exit()
		else:
			html_str = con.read().decode("utf8")
			return html_str


	def _clean_html(self, html_str):
		"""Method which preprocess the html document. Unnecessary 
		html elements such as script, style, head, comments are removed. 
		Args:
			html_str - string representation of html document
		Returns:
			BeautifulSoup object representation of html document
		"""
		html_soup = BeautifulSoup(html_str, 'html.parser')
		for element in html_soup(["script", "style", "head"]):
			element.extract()
		for element in html_soup:
			if isinstance(element, Comment):
				element.extract()

		html_soup = str(self._remove_attrs(html_soup))

		for ch in ['-', '\/']:
			html_soup = html_soup.replace(ch, " ")

		return html_soup


	def _clean_phone_numbers(self, phone_nums):
		"""Method which formats the phone numbers like it's specified
		Args:
			phone_nums - list of phone numbers
		Returns:
			list of formatted phone numbers 
		"""
		cleaned_nums = []
		for num in phone_nums:
			clean_num = re.sub(self.clean_phonenum_pattern, ' ', num)
			cleaned_nums.append(clean_num.strip())
		return cleaned_nums


	def extract_phone_numbers(self, url):
		"""Method that can be called from PhoneNumberExtractor object.
		Used to search and find phone numbers from website for the given url.
		Args:
			url - website url
		Returns:
			list of found phone numbers
		"""
		html_str = self._retrieve_html_from_url(url)

		cleaned_html = self._clean_html(html_str)

		matches = self._find_matches(cleaned_html, [self.pattern_0_a, self.pattern_0_b, self.pattern_1_a, self.pattern_1_b])
		matches = self._clean_phone_numbers(matches)
		return matches
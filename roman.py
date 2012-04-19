from collections import OrderedDict
from functools import total_ordering
from itertools import zip_longest

@total_ordering
class Letter:
	def __init__(self, letter):
		self.letter = letter

	def __eq__(self, other):
		return self.letter == other.letter

	def __lt__(self, other):
		letter_index = list(letters.keys()).index(self.letter)
		self.biggers = list(letters.values())[letter_index+1:]
		return other in self.biggers

	def __hash__(self):
		return hash(self.letter)

	def __str__(self):
		return self.letter

	def __repr__(self):
		return "Letter(%s)" % self.letter


I, V, X, L, C, D, M = [Letter(c) for c in "IVXLCDM"]

letters = OrderedDict([
	('I', I),
	('V', V),
	('X', X),
	('L', L),
	('C', C),
	('D', D),
	('M', M)
])

roman_values = {
	I: 1,
	V: 5,
	X: 10,
	L: 50,
	C: 100,
	D: 500,
	M: 1000
}

def _select_decreasing(tup):
	digits = tup[1]
	return digits[0] >= digits[1]

def _get_slice_value(digit_list):
	to_subtract = 0
	subtraction_position = [i<j for i,j in zip(digit_list, digit_list[1:])]
	if any(subtraction_position):
		i = subtraction_position.index(True) + 1
		to_subtract = sum(roman_values[d] for d in digit_list[:i])
		digit_list = digit_list[i:]
	value = sum(roman_values[d] for d in digit_list)
	return value-to_subtract

def roman_to_int(num):
	roman_digits = [letters[d] for d in num]
	indexes = filter(_select_decreasing, enumerate(zip(roman_digits, roman_digits[1:])))
	indexes = [i[0]+1 for i in indexes]
	slices = [slice(i1, i2) for i1,i2 in zip_longest([None]+indexes, indexes)]
	sliced_digits = [roman_digits[s] for s in slices]
	return sum(_get_slice_value(s) for s in sliced_digits)

int_values = [
	(1000, 'M'),
	(500, 'D'),
	(100, 'C'),
	(50, 'L'),
	(10, 'X'),
	(5, 'V'),
	(1, 'I')
]

repeatable_values = [
	(1000, 'M'),
	(100, 'C'),
	(10, 'X'),
	(1, 'I'),
	(0, '')
]


def int_to_roman(n):
	result = ""
	for v,l in int_values:
		nextv, nextl = next(filter(lambda l: l[0]<v, repeatable_values)) # subtractable_letter
		result += l * (n // v)
		n = n % v
		if n >= v - nextv:
			result += nextl+l
			n -= v - nextv
	return result
			

from unittest import TestCase, main

class TestNumbers(TestCase):
	def test_number(self):
		for i in range(10000):
			self.assertEqual(i, roman_to_int(int_to_roman(i)))

if __name__ == "__main__":
	main()

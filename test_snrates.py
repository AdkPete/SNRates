import unittest
import snrates as snr

class TestSNRMethods(unittest.TestCase):

	def test_IMF(self):
		##Test code to compute coefficients based on IMF
		
		k_cc = snr.imf()
		
		self.assertEqual(k_cc , .007)

if __name__ == "__main__":
	unittest.main()

import unittest
import snrates as snr

class TestSNRMethods(unittest.TestCase):

	def test_IMF(self):
		##Test code to compute coefficients based on IMF
		
		k_cc = snr.imf()
		
		self.assertAlmostEqual(k_cc , .007 , 4)

		k_a = snr.imf(M1 = 3 , M2 = 8)
		self.assertAlmostEqual(k_a , .021 , 3)
		
if __name__ == "__main__":
	unittest.main()

import unittest
import snrates as snr

class TestSNRMethods(unittest.TestCase):

	def test_IMF(self):
		##Test code to compute coefficients based on IMF
		
		k_cc = snr.imf()
		
		self.assertAlmostEqual(k_cc , .007 , 4)

		k_a = snr.imf(M1 = 3 , M2 = 8)
		self.assertAlmostEqual(k_a , .021 , 3)
		
	def test_NCC(self):
		
		kcc = snr.imf()
		
		SFR = 10
		zs = 0
		
		self.assertAlmostEqual(snr.ncc(SFR , zs , kcc = kcc) , .07 , 2)
		
	def test_SFH(self):
		SFR = 10
		zs = 0.5
		t = snr.time(zs)

		self.assertAlmostEqual(10 , snr.SFH(SFR , t , zs))
		
		
		
	def test_NIa(self):
		
		zs = 0.93
		SFR = 5.3
		self.assertAlmostEqual(snr.ncc(SFR , zs) , .019 , 3)
		#self.assertAlmostEqual(snr.n1a(SFR , zs) , .0023 , 4)
		self.assertAlmostEqual(snr.n1a(6.3 , 0.63) , .0035 , 4)
if __name__ == "__main__":
	unittest.main()

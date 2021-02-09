import unittest
import snrates as snr
import integrator as integ

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
		
		
class TestIntegratorMethods(unittest.TestCase):

		
	def test_squad(self):
		
		def f1(x):
			return x
		##Test integration over f(x) = x from 0 to 1
		self.assertAlmostEqual(0.5 , integ.squad(f1 , 0 , 1))
		

if __name__ == "__main__":
	unittest.main()

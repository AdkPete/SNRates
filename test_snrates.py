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
		
		self.assertAlmostEqual(snr.ncc(SFR , 0 , zs , kcc = kcc)[0] , .07 , 2)
		
	def test_SFH(self):
		SFR = 10
		zs = 0.5
		t = snr.time(zs)

		self.assertAlmostEqual(10 , snr.SFH(SFR , t , zs))
		
		
		
	def test_NIa(self):
		
		zs = 0.93
		SFR = 5.3
		alpha = -0.1895318717883241
		self.assertAlmostEqual(snr.ncc(SFR ,0, zs)[0] , .019 , 3)
		self.assertAlmostEqual(snr.n1a(SFR ,0, zs)[0], .0023 , 4)
		
	def test_sources(self):
		zs = 0.93
		SFR = 5.3
		SFR_err = .01
		alpha = -0.1895318717883241
		
		sample_source = snr.source("Sample" , 20 , zs  , SFR , SFR_err)
		self.assertAlmostEqual(sample_source.ncc , .019 , 3)
		self.assertAlmostEqual(sample_source.n1a , .0023 , 4)
		
		
		
class TestIntegratorMethods(unittest.TestCase):

		
	def test_squad(self):
		
		def f1(x):
			return x
		##Test integration over f(x) = x from 0 to 1
		self.assertAlmostEqual(0.5 , integ.squad(f1 , 0 , 1))
		
	def test_rrect(self):
		
		def f1(x):
			return x
		##Test integration over f(x) = x from 0 to 1
		self.assertAlmostEqual(0.5 , integ.right_rect(f1 , 0 , 1 , N = 100000) , 4)
		
	def test_comp(self):
		def f1(x):
				return x
		
		##Test integration over f(x) = x from 0 to 1
		self.assertAlmostEqual(0.5 , integ.composite(f1 , 0 , .1 , 1 , 100000))

		

if __name__ == "__main__":
	unittest.main()

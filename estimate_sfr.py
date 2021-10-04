import numpy as np
import astropy.units as u
from astropy.cosmology import WMAP9 as cosmo
import scipy.integrate as integrate
import integrator as integ
from astropy.cosmology import FlatLambdaCDM ,  z_at_value , Planck15

cosmo = Planck15 

def imf(M1 = 8 , M2 = 50 , Mmin = 0.1 , Mmax = 125):

	'''
	Computes IMF based coefficients for sn rate computations
	see Shu et al 2018 (Default values from here)

	'''

	##Using a salpeter IMF

	def phi(M):
		return M ** -2.35
	sn_candidates = integrate.quad(phi , M1 , M2  )[0]

	def mphi(M):
		return M * phi(M)
	total = integrate.quad(mphi , Mmin , Mmax)[0]
	return sn_candidates / total

def SFH(SFR , t , zs):

	SFH = SFR *  ( ( (1 + red(t)) / (1 + zs)) ** 2.7 )
	SFH *= (1 +  ( ( 1 + zs) / 2.9 ) ) ** 5.6 
	SFH /= (1 + (1 + red(t) ) / 2.9 ) ** 5.6

	return SFH
	
def red(t):
	t *= u.Gyr
	z = z_at_value(cosmo.age , t)
	return z
	
def fD(td):

	return td ** (-1.07)
def ncc(SFR , z, SFR_err = None, kcc = None):
	'''
	computes core collapse sn rate
	returns [ Ncc , Ncc_err ]
	'''
	
	if SFR_err == None:
		SFR_err = 0.25 * SFR

	if kcc == None:
		kcc = imf()
		
	return SFR * kcc / (1 + z) , SFR_err * kcc / (1 + z)
	
def time(z):
	#t0 = cosmo.age(z = 0).to(u.Gyr).value
	return cosmo.age(z).to(u.Gyr).value

def n1a(SFR , z , eta = 0.04 , SFR_err = None , CIa = None):

	'''
	computes an expected Type Ia supernova rate based on the redshift and star formation rate
	returns the sn rate
	'''

	if SFR_err == None:
		SFR_err = 0.25 * SFR
		
	if CIa == None:
		CIa = imf(M1 = 3 , M2 = 8)	
		
	def integrand_1(td):
		return SFH(SFR , time(z) - td , z) * fD(td)

	tmin = 1e-5
	top_int = integ.composite(integrand_1 , 0 , tmin , time(z) , N = 50)

	bottom_int = integ.composite(fD , 0 , tmin , time(0) , N = 50	)
	zs = z
	NIA= eta * CIa * top_int / ( ( 1 + zs ) * bottom_int)
	return NIA , NIA * SFR_err / SFR


Ha = [33.6 , 13.2 , 476.4 , 23.4 , 20.0 , 55.5]
z = [0.790 , 0.856 , .063 , .448 , 0.402 , .657]
Ha = 1e-17 * np.array(Ha) * u.erg / (u.s * u.cm * u.cm)
z = np.array(z)
SDSS_area = (2.5 * u.m/ 2.0) ** 2 * np.pi

#Ha *= SDSS_area.to(u.cm**2)
halphas_ls=[]
for i in range(len(Ha)):

	d = cosmo.luminosity_distance(z[i])

	na = Ha[i] * 4 * np.pi * d.to(u.cm) ** 2 / ( (1+z[i])**3)
	halphas_ls.append((na/1.26e41 ).value)
	print ( (na/1.26e41 ).value)
	
a = np.array(halphas_ls)

print (np.mean(halphas_ls))

snr_cc = []
snr_cc_err = []



for i in range(len(a)):
	
	snr , snr_err = ncc(a[i],z[i])
	snr_cc.append(snr)
	snr_cc_err.append(snr_err)
	
snr_1a = []
snr_1a_err = []

for i in range(len(a)):

	snr , snr_err = n1a(a[i],z[i])
	snr_1a.append(snr)
	snr_1a_err.append(snr_err)



print ("Total SNR : {} +- {}".format(np.mean(snr_1a) + np.mean(snr_cc) , np.mean(snr_1a_err) + np.mean(snr_cc_err)))
print ("SNR Ia : {} +- {}".format(np.mean(snr_1a) , np.mean(snr_1a_err)))

print ("SNR CC : {} +- {}".format(np.mean(snr_cc) , np.mean(snr_cc_err)))
print (np.mean(snr_cc) , np.mean(snr_1a) , np.mean(snr_1a) + np.mean(snr_cc))

import numpy as np
from read_slate import *
import scipy.integrate as integrate
from astropy.cosmology import FlatLambdaCDM ,  z_at_value , Planck15
import astropy.units as u
import integrator as integ
from os import path
import datetime
from read_slate import get_obs
cosmo = Planck15 #FlatLambdaCDM(H0=67.8, Om0=0.308)

###Created by Peter Craig
###pac4607@rit.edu


###TODO:
###Fix SN rates, probably via calculating them from the SFR
###Provide a proper detection efficiency (should include effects from our program's cadence)



include_core_collapse = True ## if true, we include the core collapse sn rate in our rate calculations.
## This includes an adjustment to the magnitudes to account for the difference in absolute magnitudes between SN types
class source:
	###A class to hold useful info for each source
	##Contains the ID, peak r band apparent magnitude (m_r) , type Ia SN rate (n1a) , core collapse SN rate (ncc)
	def __init__(self , ID , m_r , zs , SFR , SFR_err , n1a , n1a_err , ncc , ncc_err):
		self.ID = ID
		self.m_r = m_r
		self.ncc = 0
		self.n1a = 0
		self.zs = zs
		self.sfr = SFR
		self.sfr_err = SFR_err

		self.ncc = ncc
		self.ncc_err = ncc_err
		self.n1a = n1a
		self.n1a_err = n1a_err
		
		#self.compute_snrates()
		
	def compute_snrates(self):
		
		ncc_vals = ncc(self.sfr , self.sfr_err, self.zs)
		n1a_vals = n1a(self.sfr , self.sfr_err, self.zs)
		self.ncc = ncc_vals[0]
		self.ncc_err = ncc_vals[1]
		self.n1a = n1a_vals[0]
		self.n1a_err = n1a_vals[1]
	

def read(rescale=True):
	'''
	returns a list of source objects
	reads in the source_data.txt file, and provides the required information
	'''

	
	fname = "source_data.txt"
	'''
	npfname = "sources.npy"
	if path.exists(npfname):
		print ("reading sources from numpy file")
		a = np.load(npfname , allow_pickle = True)
		
		return a
	'''
	
	f = open(fname)
	 
	sources = []
	tsnr = 0
	for i in f.readlines(): ##Iterate through the lines in the file
	
		##Grabs relevant quantities
		a = i.split("|")
		name = a[18]
		ra = a[3]
		dec = a[4]
		zs = a[6]
		ncc = a[13]
		ncc_err = a[14]
		n1a = a[15]
		n1a_err = a[16]
		m_r = a[19]
		SFR = a[11]
		SFR_err = a[12]
		
		if a[0] == "Survey":
			continue
		
		## convert to floats, and set missing sn rates to 0. There is only one source that actually triggers this,
		## which is the SWELLS source, which is also lacking a SFR
		m_r = float(m_r)
		zs = float(zs)
		try:
			SFR = float(SFR)
			SFR_err = float(SFR_err)
			n1a = float(n1a)
			n1a_err = float(n1a_err)
			ncc = float(ncc)
			ncc_err = float(ncc_err)
			
		except:
			SFR = 0
			SFR_err = 0
			n1a = 0
			n1a_err = 0
			ncc = 0
			ncc_err = 0
			
		if rescale:
			n1a /= (1 + zs) ** 2
			n1a_err /= (1 + zs) ** 2
			ncc /= (1 + zs) ** 2
			ncc_err /= (1 + zs) ** 2
		
		sources.append(source(name , m_r , zs , SFR , SFR_err , n1a , n1a_err , ncc , ncc_err))
		tsnr += n1a + ncc
	print ("total snr is {}".format(tsnr))
	#np.save(npfname , sources)
	return sources
		
def detection_rate(slist , detection_efficiency):
	'''
	Takes in a list of source objects, and a function called detection_efficiency
	This function should take in a peak magnitude, and return a probability of detection
	Uses the provided sn rates to estimate our detection  rate
	'''
	
	
	expected_rate = 0
	N = 0
	for i in sl:
		if i.m_r < 20.8:
			N += 1
			
		if include_core_collapse:
			expected_rate += detection_efficiency(i) * (i.n1a / (1 + i.zs)) + i.ncc * detection_efficiency(i , CC = True)
		else:
			expected_rate += detection_efficiency(i) * (i.n1a / (1 + i.zs))
	print ("Our expected detection rate is {} per year".format(expected_rate))

	
	
def theoretical_de(source , CC = False):
	'''
	This is an over-simplified detection efficiency.
	Uses a step function, returns 0 at magnitudes greater than some threshold, 1 otherwise.
	'''
	
	avg_cadence = np.mean(get_obj_cadence(source.ID))
	
	typical_worst_case = avg_cadence / 2.0 ##Largest distance from peak
	
	mag = source.m_r + typical_worst_case.days * .03 ##FIXME, pull better value for SN light curve, improve cadence handling.
	m50 = 22.5
	if mag <= m50 and not CC:
		return 1
	elif source.m_r + 1.5 < m50 and CC:
		return 1
	
	return 0
	
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
	
def ncc(SFR ,SFR_err, z, kcc = None):
	'''
	computes core collapse sn rate
	returns [ Ncc , Ncc_err ]
	'''
	
	if kcc == None:
		kcc = imf()
		
	return [ SFR * kcc / (1 + z) , SFR_err * kcc / (1 + z) ]

def red(t):
	t *= u.Gyr
	z = z_at_value(cosmo.age , t)
	return z
	
def time(z):
	#t0 = cosmo.age(z = 0).to(u.Gyr).value
	return cosmo.age(z).to(u.Gyr).value
	
	
def SFH(SFR , t , zs):

	SFH = SFR *  ( ( (1 + red(t)) / (1 + zs)) ** 2.7 )
	SFH *= (1 +  ( ( 1 + zs) / 2.9 ) ) ** 5.6 
	SFH /= (1 + (1 + red(t) ) / 2.9 ) ** 5.6
	
	return SFH
	
	
def fD(td):

	return td ** (-1.07)
	
	
def n1a(SFR , SFR_err , z , eta = 0.04 , CIa = None):

	'''
	computes an expected Type Ia supernova rate based on the redshift and star formation rate
	returns the sn rate
	'''
	
	if CIa == None:
		CIa = imf(M1 = 3 , M2 = 8)	
		
	def integrand_1(td):
		return SFH(SFR , time(z) - td , z) * fD(td)
	
	tmin = 1e-5
	top_int = integ.composite(integrand_1 , 0 , tmin , time(z) , N = 50)
	
	bottom_int = integ.composite(fD , 0 , tmin , time(0) , N = 50	)
	zs = z
	NIA= eta * CIa * top_int / ( ( 1 + zs ) * bottom_int)
	return [ NIA , NIA * SFR_err / SFR ]
	
def model_1(sources):

	''' 
	Over-simplifide model. Assumes that we get 100% coverage and
	100% detection efficiency on all sources
	'''
	
	survey_length = 2
	N = 0
	N_err = 0
	for i in sources:
		N += i.ncc + i.n1a
		if not (np.isnan(i.ncc_err) or (np.isnan(i.n1a_err))):
			N_err += i.ncc_err ** 2 + i.n1a_err ** 2
		
	return N * survey_length , survey_length * np.sqrt(N_err)

def model_2(sources , de):
	'''
	Simple model. Assumes 100% coverage, uses real detection efficiency curves
	'''
	survey_length = 1.0
	N = 0
	N_err = 0
	for i in sources:
		N += i.ncc * de(i.m_r + 1.5) + i.n1a * de(i.m_r)
		if not (np.isnan(i.ncc_err) or (np.isnan(i.n1a_err))):
			N_err += (i.ncc_err * de(i.m_r + 1.5)) ** 2 + (i.n1a_err * de(i.m_r)) ** 2
	return N * survey_length , survey_length * np.sqrt(N_err)
	

def model_3(sources , de):
	'''
	Full snrate model
	'''
	
	start = datetime.datetime(2018,12,31 , 0 , 0 , 0 , tzinfo = datetime.timezone.utc)
	
	end = datetime.datetime(2019 , 12 ,  31 , 0 , 0 ,0 , tzinfo = datetime.timezone.utc)
	inc = datetime.timedelta(days = 1.0)
	
	N_err = 0
	N = 0
	Ncc = 0
	N1a = 0
	Nccerr = 0
	N1aerr = 0
	
	##Iterate over all sources in our sample
	for i in sources:
		obs = np.array(get_obs(i.ID))
		day = start
		
		##Sum expected yield from each day 
		while day <= end:
			time_to_obs = np.amin(abs(obs - day))
			
			fcc = de(i.m_r , time_to_obs.days , cc = True)
			f1a = de(i.m_r , time_to_obs.days)
			
			fcc_err = 0.1
			f1a_err = 0.1
			Ncc += i.ncc * fcc / 365.0
			N1a += i.n1a * f1a / 365.0
			N1aerr  += i.n1a_err ** 2
			Nccerr  += i.ncc_err ** 2
			N += ( i.ncc * fcc + i.n1a * f1a) * 1 / 365.0
			if not (np.isnan(i.ncc_err) or (np.isnan(i.n1a_err))):
				N_err +=  (i.ncc_err ) ** 2 + (i.n1a_err) ** 2  + (i.ncc * f1a_err) ** 2 + (i.n1a * fcc_err ) ** 2
			day += inc
			
			
	print (Ncc, np.sqrt(Nccerr / 365))
	print (N1a , np.sqrt(N1aerr / 365))
	
	return N, np.sqrt(N_err) / np.sqrt(365)
	
if __name__ == "__main__":
	## Kyle's number: 1.1
	sl = read(rescale = True)
	def kde(m , t = 0 , cc = False):
		if cc:
			m += 1
		
		m += t * 0.1
		if m > 23:
			return 0
		elif m > 22.5:
			return 0.2
		elif m > 22:
			return 0.5
		elif m > 21.5:
			return 0.75
		return 1
		
	def final_de(m , t=0 , cc = False):
		if cc:
			m += 1.75
		
		m += t * 0.087
		mlim = 24.7
		m50 = mlim-1.5
		alpha = 1.85
		
		
		return 1.0/( 1 + np.exp(alpha * ( m-m50 ) ))
		
	def toy_de(m , t = 0 , cc = False):
		if cc:
			m += 1
		m += t * 0.087
		if m > 24:
			return 0
		return 1
		
	N,Nerr = model_3(sl , final_de)
	print (N,Nerr)
	'''
	err = 0
	for i in sl:
		if np.isnan(i.n1a_err):
			continue
		err += i.ncc_err ** 2 + i.n1a_err ** 2
	
	print (err)
	'''

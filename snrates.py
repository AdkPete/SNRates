import numpy as np
from read_slate import *

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
	def __init__(self , ID , m_r , ncc , n1a , zs , SFR):
		self.ID = ID
		self.m_r = m_r
		self.ncc = ncc
		self.n1a = n1a
		self.zs = zs
		self.sfr = SFR
	

def read():
	'''
	returns a list of source objects
	reads in the source_data.txt file, and provides the required information
	'''
	
	
	fname = "source_data.txt"
	
	f = open(fname)
	 
	sources = []
	for i in f.readlines(): ##Iterate through the lines in the file
	
		##Grabs relevant quantities
		a = i.split("|")
		name = a[18]
		ra = a[3]
		dec = a[4]
		zs = a[6]
		ncc = a[13]
		n1a = a[15]
		m_r = a[19]
		SFR = a[11]
		
		
		if a[0] == "Survey":
			continue
		
		## convert to floats, and set missing sn rates to 0. There is only one source that actually triggers this,
		## which is the SWELLS source, which is also lacking a SFR
		m_r = float(m_r)
		zs = float(zs)
		try:
			n1a = float(n1a)
		except:
			n1a = 0
			
		try:
			ncc = float(ncc)
		except:
			ncc = 0
		sources.append(source(name , m_r , ncc , n1a , zs , SFR))
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
	see Shu et al 2018 (Default values from here
	'''
	
	return 0


if __name__ == "__main__":
	## Kyle's number: 1.1
	sl = read()
	detection_rate(sl , theoretical_de)
	

import numpy as np

###Created by Peter Craig
###pac4607@rit.edu


###TODO:
###Fix SN rates, probably via calculating them from the SFR
###Provide a proper detection efficiency (should include effects from our program's cadence)

cadence_correction = 0.3 ##FIXME, may not be the best cadence handling.
class source:
	###A class to hold useful info for each source
	##Contains the ID, peak r band apparent magnitude (m_r) , type Ia SN rate (n1a) , core collapse SN rate (ncc)
	def __init__(self , ID , m_r , ncc , n1a , zs):
		self.ID = ID
		self.m_r = m_r
		self.ncc = ncc
		self.n1a = n1a
		self.zs = zs
	

def read():
	
	fname = "source_data.txt"
	
	f = open(fname)
	
	sources = []
	for i in f.readlines():
		a = i.split("|")
		name = a[18]
		ra = a[3]
		dec = a[4]
		zs = a[6]
		ncc = a[13]
		n1a = a[15]
		m_r = a[19]
		
		if a[0] == "Survey":
			continue
			
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
		sources.append(source(name , m_r , ncc , n1a , zs ))
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
			
		##Uncomment second half of this line to include core collapse supernovae.
		expected_rate += detection_efficiency(i.m_r + cadence_correction) * (i.n1a / (1 + i.zs))# + i.ncc * detection_efficiency(i.m_r + 2)
	print ("Our expected detection rate is {} per year".format(expected_rate))

	
	
def theoretical_de(mag):
	'''
	This is an over-simplified detection efficiency.
	Uses a step function, returns 0 at magnitudes greater than some threshold, 1 otherwise.
	'''
	if mag <= 22:
		return 1
	return 0


if __name__ == "__main__":
	
	sl = read()
	detection_rate(sl , theoretical_de)

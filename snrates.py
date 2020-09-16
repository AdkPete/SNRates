import numpy as np

###Created by Peter Craig
###pac4607@rit.edu


###TODO:
###Fix SN rates, probably via calculating them from the SFR
###Provide a proper detection efficiency (should include effects from our program's cadence)
class source:
	###A class to hold useful info for each source
	##Contains the ID, peak r band apparent magnitude (m_r) , type Ia SN rate (n1a) , core collapse SN rate (ncc)
	def __init__(self , ID , m_r , ncc , n1a):
		self.ID = ID
		self.m_r = m_r
		self.ncc = ncc
		self.n1a = n1a
		
	

def read(): ##Reads in data file
	
	our_ids = []
	magnitudes = []
	
	##Somewhat suboptimum, but reading in two files lets us filter out sources
	##which are outside of our sample.
	
	fname_1 = "peak_mags.txt" ##Data file with the same info as the google sheet
	fname_2 = "all_data.txt" ##Data file with all relevent info (and some extra) from Yiping's Paper
		
	f = open(fname_1)
	
	##First we read in peak_mags, mostly to get a list of source id's that are in our search program.

	for i in f.readlines():
		a = i.split()
		if a[0] == "Source":
			continue
		our_ids.append(a[0])
		magnitudes.append(float(a[4]))
	
	f.close()
	
	f = open(fname_2)
	
	##Read through second file, gather all info for our sources
	
	source_list = []

	##This bit is somewhat messsy, but it is functional
	for i in f.readlines():
		a = i.split("|")
		if len(a) < 3:
			continue
		if "SWELLS" + a[1] in our_ids:
			ID = "SWELLS" + a[1]
			m_r = magnitudes[our_ids.index(ID)]
			try:
				ncc = float(a[13])
			except:
				ncc = 0
				
			try:
				n1a = float(a[15])
			except:
				n1a = 0
			source_list.append(source(ID , m_r , ncc , n1a))
			
		if "SDSS" + a[1] in our_ids:
			ID = "SDSS" + a[1]
			m_r = magnitudes[our_ids.index(ID)]
			try:
				ncc = float(a[13])
			except:
				ncc = 0
				
			try:
				n1a = float(a[15])
			except:
				n1a = 0
			source_list.append(source(ID , m_r , ncc , n1a))
			
		if "BELLS" + a[1] in our_ids:
			ID = "BELLS" + a[1]
			m_r = magnitudes[our_ids.index(ID)]
			try:
				ncc = float(a[13])
			except:
				ncc = 0
			try:
				n1a = float(a[15])
			except:
				n1a = 0
			source_list.append(source(ID , m_r , ncc , n1a))
			
	
	return source_list
	
	
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
			
	
		expected_rate += detection_efficiency(i.m_r) * (i.n1a) + i.ncc * detection_efficiency(i.m_r + 2)
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

import numpy as np

class source:
	###A class to hold useful info for each source
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
	
	fname_1 = "peak_mags.txt"
	fname_2 = "all_data.txt"
		
	f = open(fname_1)

	for i in f.readlines():
		a = i.split()
		if a[0] == "Source":
			continue
		our_ids.append(a[0])
		magnitudes.append(float(a[4]))
	
	f.close()
	
	f = open(fname_2)
	
	#print (our_ids)
	
	source_list = []

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
	print (len(our_ids) , len(source_list))
	
def detection_rate(slist , detection_efficiency):
	
	expected_rate = 0
	N = 0
	for i in sl:
		if i.m_r < 20.8:
			N += 1
			
	
		expected_rate += detection_efficiency(i.m_r) * (i.n1a) + i.ncc * detection_efficiency(i.m_r + 2)
	print (expected_rate)
	print (N)
	
	
def theoretical_de(mag):

	if mag < 20.8:
		return 1
	return 0

	
sl = read()
print (len(sl))
detection_rate(sl , theoretical_de)

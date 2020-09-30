
import pickle , datetime

fname = "slate.dat"

f = open(fname , "rb")
serial = pickle.load(f)

def get_obs(source_id):

	for k, d in serial['objects'].items():
		## k is the name of the object
		## d contains info for every obs request of this source
		
		if k != source_id: ## Skip all sources other that the one we want
			continue
		
		all_obs = d['obs'] ##Info for all obs requsts.
		
		observation_dates = [] ##Will be a list of all completed observations of this source
		
		for i in all_obs:
			if i['state'] == 'COMPLETED':
				observation_dates.append(i['completed'])
				
		observation_dates.sort()
		return observation_dates
		
if __name__ == "__main__":

	obs_dates = get_obs("SDSSJ1432+6317")
	
	print (obs_dates)

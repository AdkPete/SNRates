
import pickle , datetime
import numpy as np
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
		
def get_obj_cadence(source_id):

	obs_dates = get_obs(source_id)
	
	times = []
	
	for i in range(len(obs_dates) - 1): ##We iterate through the dates, but not the last one (as there is no time between that and the next one
	
		times.append(obs_dates[i+1]  - obs_dates[i])
		
	return times
		
if __name__ == "__main__":

	obs_dates = get_obs("SDSSJ1432+6317")

	get_obj_cadence("SDSSJ1432+6317")

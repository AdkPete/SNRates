
import numpy as np
import scipy


def squad(f , xmin  , xmax):
	'''
	Performes numerical quadrature on the given function
	Uses scipy quadrature package
	evaluates the integral of f(x) from xmin to xmax
	
	Parameters
	__________
	
	f : function : The function to be integrated. Should take one argument
	xmin : float : Lower integration bound
	xmax : float : Upper integration bound

	Returns
	_______
	
	Returns the value of the computed integral
	
	'''
	
	res = scipy.integrate.quad(f , xmin , xmax)[0]
	return res

def right_rect(f , xmin  , xmax , N = 100000):
	'''
	Performes numerical quadrature on the given function
	Uses a right-evaluated rectangle rule
	evaluates the integral of f(x) from xmin to xmax

	Parameters
	__________

	f : function : The function to be integrated. Should take one argument
	xmin : float : Lower integration bound
	xmax : float : Upper integration bound

	Returns
	_______

	Returns the value of the computed integral

	'''
	
	

	res = 0
	
	dx = float(xmax - xmin ) / N
	
	x = xmin
	while x + dx <= xmax:
		
		res += f(x + dx) * dx
		x += dx
	if x < xmax:
		width = xmax - x
		res += f(xmax) * width
	
	return res

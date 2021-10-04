
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

def right_rect(f , xmin  , xmax , N = 1000):
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

def composite(f , xminr , xmin , xmax, N = None):
	
	'''
	Performes numerical quadrature on the given function
	Uses a combination of squad and right rectangle
	
	evaluates the integral of f(x) from xmin to xmax

	Parameters
	__________

	f : function : The function to be integrated. Should take one argument
	xmin : float : Lower integration bound for squad
	xmax : float : Upper integration bound for squad
	xminr : float : Lower integration bound for right rectangle

	Returns
	_______

	Returns the value of the computed integral

	'''
	
	res = squad(f , xmin , xmax)
	if N == None:
		res += right_rect(f , xminr , xmin)
	else:
		res += right_rect(f, xminr , xmin , N)
	return res

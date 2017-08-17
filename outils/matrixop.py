# coding: utf-8

#########################################################################
#																		#
#							matrixop.py									#
#																		#
#			Opération sur matrice				 						#
#			exemple: comatrice (car pas présent dans numpy)				#
#																		#
#			Auteur : ................. Cavron Jérémy					#
#			Date de création : ....... 16/08/2017						#
#			Date de modification : ... 16/08/2017						#
#																		#
#			Portfolio : www.dbs.bzh/portfolio 							#
#########################################################################

#--- les imports ---
from numpy import linalg

def comatrix(matrix, det):
	return linalg.inv(matrix)/(1/det)
#!/bin/python

import numpy as np
import string

class ChessBoard:
	def __init__(self):
		self.board=[[' '  for i in np.arange(8)] for j in np.arange(8)]
		#self.board=[ {j:'A' for j in string.ascii_lowercase[:8]} for i in np.arange(8)]

#	def display(self):
		

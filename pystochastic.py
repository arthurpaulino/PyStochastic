from fractions import Fraction
import numpy as np

class PyStochastic:
	def __init__(self):
		self.__states__ = set()
		self.__weight__ = {}
		self.ready = False
	
	def __frac__(self, x):
		return Fraction(x).limit_denominator()
		
	def __complete__(self):
		for r in self.__states__:
			for s in self.__states__:
				if not self.__weight__.has_key((r,s)):
					self.__weight__[(r,s)] = 0.0
		self.ready = True

############ Chain Management
	
	def link(self, r, s, p):
		if r not in self.__states__:
			self.__states__.add(r)
		if s not in self.__states__:
			self.__states__.add(s)
		self.__weight__[(r,s)] = p
		self.ready = False
	
	def prt(self):
		if not self.ready:
			self.__complete__()
		print '-------------------------------Markov Chain------------------------------'
		for r in self.__states__:
			for s in self.__states__:
				w = self.__weight__[(r,s)]
				if w > 0.0:
					print '{}->{}: {}'.format(r,s,self.__frac__(w))

############ Computations
	
	def __out_matrix__(self, row_states, column_states):
		if not self.ready:
			self.__complete__()
		A = []
		for r in row_states:
			line = []
			for s in column_states:
				line.append(self.__weight__[(r,s)])
			A.append(line)
		return np.matrix(A)
	
	def __in_matrix__(self, row_states, column_states):
		if not self.ready:
			self.__complete__()
		A = []
		for r in row_states:
			line = []
			for s in column_states:
				line.append(self.__weight__[(s,r)])
			A.append(line)
		return np.matrix(A)
	
	def __transient__(self, state):
		for s in self.__states__:
			if state != s and self.__weight__[(state,s)] != 0.0:
				return False
		return True
	
	def __transiency_partition__(self):
		if not self.ready:
			self.__complete__()
		non_transient_states = set()
		transient_states = set()
		for state in self.__states__:
			if self.__transient__(state):
				transient_states.add(state)
			else:
				non_transient_states.add(state)
		return (non_transient_states, transient_states)
	
	def __print__(self, matrix, rows, columns):
		s = '\t'
		for column in columns:
			s += str(column)+'\t'
		print s
		i = 0
		for row in rows:
			s = str(row)+'\t'
			j = 0
			for column in columns:
				s += str(self.__frac__(matrix.item((i,j))))+'\t'
				j += 1
			print s
			i += 1
	
	def compute(self):
	
		(non_transient_states, transient_states) = self.__transiency_partition__()
		
		if len(transient_states) == 0:
			A = self.__in_matrix__(self.__states__, self.__states__) - np.identity(len(self.__states__))
			A = np.delete(A, 0, 0)
			A = np.append(A, [np.ones(len(self.__states__))], 0)
			b = np.zeros(len(self.__states__)-1)
			b = np.append(b,1.0)
			sol = np.linalg.solve(A, b)
			print '---------------------------Wandering Proportions-------------------------'
			for state, proportion in zip(self.__states__, sol):
				print '{}: {}'.format(state, self.__frac__(proportion))
				for s in self.__states__:
					prop = proportion*self.__weight__[(state, s)]
					if prop > 0.0:
						print '\t{}->{}: {}'.format(state, s, self.__frac__(proportion*self.__weight__[(state, s)]))
		else:
			Q = self.__out_matrix__(non_transient_states, non_transient_states)
			I = np.identity(len(non_transient_states))
			print 'Number of visits to [column], before absortion, when starting from [line]'
			V = np.linalg.inv(I - Q)
			self.__print__(V, non_transient_states, non_transient_states)
			print 'Probability of absortion in [column] when starting from [line]'
			R = self.__out_matrix__(non_transient_states, transient_states)
			A = V*R
			self.__print__(A, non_transient_states, transient_states)
	
	def wander(self, pi, n):
		P = self.__out_matrix__(self.__states__, self.__states__)
		p = []
		for state in self.__states__:
			if pi.has_key(state):
				p.append(pi[state])
			else:
				p.append(0.0)
		p = np.matrix(p)
		for i in range(n):
			p = p*P
		pi = {}
		print '----------------------------Wandering Result----------------------------'
		for state, i in zip(self.__states__, range(len(self.__states__))):
			print '{}: {}'.format(state, p.item(i))
			pi[state] = p.item(i)
		return pi

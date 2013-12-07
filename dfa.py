import re
from random import randrange,choice
from abc import ABCMeta, abstractmethod

class DFATrapException(Exception):
    def __init__(self, message):
        super(DFATrapException, self).__init__(message)
        self.message = message
class InvalidDFADescriptionException(Exception):
    def __init__(self, message):
        super(InvalidDFADescriptionException, self).__init__(message)
        self.message = message
class DFATestFailedException(Exception):
    def __init__(self, message):
        super(DFATestFailedException, self).__init__(message)
        self.message = message

def split(s):
	return s.split(',')

def parse_transition(s):
	match=re.match('(.*),(.*)->(.*)',s)
	if match==None:
		raise InvalidDFADescriptionException("Illegal transition %s"%s)
	return re.match('(.*),(.*)->(.*)',s).groups()

def bool_to_accepts(b):
	return 'Accepts' if b else 'Rejects'
	
class abstractFSM:
	__metaclass__ = ABCMeta
	
	def __init__(self,name,filename,debug=False):
		dfa_desc=[line.replace('\n','') for line in open(filename,'r').readlines() if len(line.strip())>0 and not line[0]=='#']
		self.name=name
		self.debug=debug
		self.alphabet=split(dfa_desc[0])
		self.states=split(dfa_desc[1])
		self.start=dfa_desc[2]
		self.accept=split(dfa_desc[3])
		self.transitions=[parse_transition(t) for t in dfa_desc[4:]]
		if not self.start in self.states:raise InvalidDFADescriptionException('Invalid starting state %s'%start)
		if not set(self.accept).issubset(set(self.states)):raise InvalidDFADescriptionException('Not all acceptance states were predefined as valid states')
	@abstractmethod
	def move(self,state,letter):
		pass
	@abstractmethod
	def simulate(self,s):
		pass
	def rand_string(self,maxlength):
		s=''
		for i in range(randrange(maxlength+1)):
			s+=choice(self.alphabet)
		return s
		
	def test(self,predicate,tests=1000,maxstringlength=20):
		print 'Testing "%s"...'%self.name
		for i in range(tests):
			s=self.rand_string(maxstringlength)
			simresult,predresult=self.simulate(s),predicate(s)
			if simresult!=predresult:
				print 'Test failed.'
				print 'Input string "%s"'%s
				print 'DFA:\t\t%s.'%bool_to_accepts(simresult)
				print 'Predicate:\t%s.'%bool_to_accepts(predresult)
				return
		print 'Success! The state machine and the predicate agreed on %d tests.'%tests
		
class dfa(abstractFSM):
	def move(self,state,letter):
		nexts=[n for i,l,n in self.transitions if i==state and l in (letter,'*')]
		if len(nexts)==0:
			raise DFATrapException('No transition defined for (%s,%s)'%(state,letter))
		if self.debug:print '%s,%s->%s'%(state,letter,nexts[0])
		return nexts[0]
		
	def simulate(self,s):
		if self.debug: print 'Simulating %s on input %s:'%(self.name,s)
		state=self.start
		result=None
		try:
			for c in s:
				state=self.move(state,c)
			result=state in self.accept
		except DFATrapException:
			result=False
		if self.debug: print bool_to_accepts(result)
		return result
		
class nfa(abstractFSM):
	def move(self,state,letter):
		nexts=set([n for i,l,n in self.transitions if i==state and l in (letter,'*')])
		if len(nexts)==0:
			raise DFATrapException('No transition defined for (%s,%s)'%(state,letter))
		if self.debug:print '%s,%s->{%s}'%(state,letter,",".join(list(nexts)))
		return nexts
	def simulate(self,s):
		if self.debug: print 'Simulating %s on input %s:'%(self.name,s)
		states={self.start}
		result=None
		for c in s:
			nexts=set()
			for state in states:
				try:
					nexts=nexts.union(self.move(state,c))
				except DFATrapException:
					pass
			states=nexts
		result=len(states.intersection(self.accept))>0
		if self.debug: print bool_to_accepts(result)
		return result
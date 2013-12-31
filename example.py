from fasim import nfa

# First, we construct the nfa from the description file:
foo_nfa=nfa('A sample nfa','example.nfa')
# Next, we create a Python String->Boolean function that checks whether a string over our alphabet is in the language:
foo_predicate=lambda s: '101' in s

# Now, let's test our machine!
foo_nfa.test(foo_predicate,10000) # 10000 is the number of tests we're about to perform
# Output:
# 	Testing "A sample nfa"...
# 	Success! The state machine and the predicate agreed on 10000 tests.

# But what happens when we're wrong? Let's modifiy the predicate a little:
foo_predicate=lambda s: '1010' in s
foo_nfa.test(foo_predicate) # The default number of tests is 1000
# Output:
# 	Testing "A sample nfa"...
#	Test failed.
#	Input string "1011011"
#	DFA:            Accepts.
#	Predicate:      Rejects.
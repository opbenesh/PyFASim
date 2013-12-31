### PyFASim - A simple Python library for simulating and unit testing finite state machines ###

This program enables simulation and testing on finite state machines.

Testing process:

1. Describe the machine in a seperate file.
2. Write a Python String->Bool function that checks whether a string over the alphabet is valid
3. Test it using the library
4. Profit!

PyFASim generates random strings over the given alphabet. Every string is fed to the state nmachine and the predicate, and the results are compared.
If a mismatch is found, the test fails and the string is presented to the user.
If the machine and the predicate agree on all of the strings - the test is successful.

"Example.py" and "Example.nfa" demonstrate using the library.

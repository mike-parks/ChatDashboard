'''
Created on Jun 13, 2014

@author: Nick
'''
import re

def validateEmail(email):
    regex_pattern = "[^@]+@[^@]+\.[^@]+"
    re.compile(regex_pattern)
    
    if not re.match(regex_pattern, email):
        return False
    else:
        return True
    
def validatePassword(password):
    regex_pattern = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    re.compile(regex_pattern)
    
    if not re.match(regex_pattern, password):
        return False
    else:
        return True
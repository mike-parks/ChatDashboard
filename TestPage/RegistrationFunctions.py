'''
Created on Jun 13, 2014

@author: Nick
'''
import re

def validateEmail(email):
    regex_pattern = "[^@]+@[^@]+\.[^@]+"
    re.compile(regex_pattern)
    
    if not re.match(email):
        return False
    else:
        return True
    
def validatePassword(password):
    regex_pattern = "^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\\d)(?=.*[!#$%&? \"]).*$"
    re.compile(regex_pattern)
    
    if not re.match(password):
        return False
    else:
        return True
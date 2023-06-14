import numpy as np

def logistic_sigmoid(x, a=1.0, b=1.0, c=0.0, d=0.0):
    """Implementation of the logistic sigmoid function with basic shape defined as y = 1/(1+exp(-x))
    
    This implementation is an extended version that allows to modify the function by applying 
    4 parameters: y = a * 1/(1+exp(b*(-x + c)) + d
    
    with parameters:
    a: modifies the amplitude of the function
    b: modifies the steepness of the function
    c: translates the function over the x axis
    d: translates the function over the y axis    
    """
    r = a * 1/(1 + np.exp(b*(-x + c))) + d
    return r    
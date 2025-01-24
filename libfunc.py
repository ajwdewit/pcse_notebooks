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


def afgen(x, table_function):
    """A simple interpolation function
    """
    if(len(table_function)%2 != 0):
        raise Exception("Error: table function should have an even number of elements")
    else:
        # Do nothing and continue; table function has an even number of elements
        pass 
    if(len(table_function) < 4):
        raise Exception("Error: table function should have at least 4 elements (2 xs and 2 ys")
    else:
        # There are at least two x-y combinations in the table function. Extract the xs and ys
        xs = [None] * int(len(table_function)/2)
        ys = [None] * int(len(table_function)/2)    
        for i in range(0, len(table_function)):
            if(i%2 == 0):
                xs[int(i/2)] = table_function[i]
            else:
                ys[int((i-1)/2)] = table_function[i]
    for i in range(1, len(xs)):
        if(xs[i] < xs[i-1]):
            raise Exception("Error: a x element of a table function cannot be smaller than the previous x")
        elif(xs[i] == xs[i-1]):
            raise Exception("Error: a x element of a table function cannot be equal to the previous x")
        else:
            # Do nothing; for each x in xs, the value of x is higher than its previous value
            pass
    if(x < xs[0]):
        x = xs[0]
        # raise Exception("Error: x is smaller than the lowest value of x in the table function")
    elif(x > xs[-1]):
        x = xs[-1]
        # raise Exception("Error: x is higher than the highest value of the x in the table function ")
    else:
        # Do nothing; for each x, the value is within of the defined range of xs in the table function.
        pass
        
    ind = 0
    x0 = xs[ind]
    x1 = xs[ind + 1]
    y0 = ys[ind]
    y1 = ys[ind + 1]
        
    while(x > x1):
        x0 = xs[ind]
        x1 = xs[ind + 1]
        y0 = ys[ind]
        y1 = ys[ind + 1]
        ind+=1
        
    y = y0 * ((x1 - x) / (x1 - x0)) + y1 * ((x - x0) / (x1 - x0))
    return y

def linear_regression(x,y):
    if len(x) is not len(y):
        return
        
    m = len(x)
    
    w1_upper = m * sum([a*b for a,b in zip(x,y)]) - (sum(x)*sum(y))
    w1_lower = m * sum([a*a for a in x]) - sum(x)*sum(x)
    w1 = w1_upper/w1_lower

    w0 = (1/m)*sum(y) - (w1/m)*sum(x)

    print("w0: ")
    print(w0)
    print("w1: ")
    print(w1)
    
x = [1,3,4,5,9]
y = [2,5.2,6.8,8.4,14.8]

linear_regression(x,y)

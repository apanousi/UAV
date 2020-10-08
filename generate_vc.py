
def generate_vc(x1,y1,x2,y2,tx1,ty1,tx2,ty2):
    dx1_tx1 = abs(x1-tx1)
    dy1_ty1 = abs(y1-ty1)
    dx2_tx2 = abs(x2-tx2)
    dy2_ty2 = abs(y2-ty2)

    s1 = (dy1_ty1)/ (dx1_tx1)
    s2 = (dy2_ty2)/ (dx2_tx2)

    c1=0
    c2=0

    ## check if their slope are the same or not, if no, that means they might have a crossing point
    if s1 != s2:

        ## computing the crossing point 
        c1 = y1-s1*x1
        c2 = y2-s2*x2
        vcx = (c2-c1)/(s1-s2)
        vcy = (c1*s2-c2*s1)/(s2-s1) 

        ## check if the crossing point is in the line segment or not (first make sure the boundaries)
        right1=0
        left1=0
        right2=0
        left2=0

        if x1 > tx1:    ###    tx1 <---> x1
            right1 = x1
            left1 = tx1

        if x1 < tx1: ###    x1 <---> tx1
            right1 = tx1
            left1 = x1

        if x2 > tx2:
            right2 = x2  ###    tx2 <---> x2
            left2 = tx2

        if x2 < tx2:  ###    x2 <---> tx2
            right2 = tx2
            left2

        ## if the crossing point is in the segments, make the crossing point as VC
        if left1 < vcx and vcx < right1 and left2 < vcx and vcx < right2:
            print("two segmented lines have a crossing point")
            return (vcx, vcy)
        else:
            print("No crossing point")

    
    ## check if their slope are the same or not, if yes check if they are parallel or overlaps
    # elif s1 == s2:
        ##check if they are parallel
        # if parallel:
        #    do nothing since they wont crash
        # else:
        # return midpoint of two drones ( (x1+x2)/2, (y1+y2)/2 )
print(generate_vc(0,0,2,-3,1,1,4,-3))
from dronekit import Vehicle, LocationGlobalRelative

def check_crossingpoint(curr1, curr2, targ1, targ2):
                         
    ## check if this crossing point is in the line segment or not (first we need to make sure the boundaries)
    
    x1 = curr1[0]
    x2 = curr2[0]
    y1 = curr1[1]
    y2 = curr2[1]
    tx1 = targ1[0]
    tx2 = targ2[0]
    ty1 = targ1[1]
    ty2 = targ2[1]

    if x1 < x2:
        ld_start_x  = x1
        ld_target_x = tx1
        
        rd_start_x  = x2        
        rd_target_x = tx2
    
    
    if x2 < x1:
        ld_start_x  = x2   
        ld_target_x = tx2
        
        rd_start_x  = x1
        rd_target_x = tx1
        
    
    right1 = 0
    left1  = 0
    right2 = 0
    left2  = 0

    ###    tx1 <---> x1
    if ld_start_x > ld_target_x:    
        right1 = ld_start_x
        left1  = ld_target_x

    ###    x1 <---> tx1
    if ld_start_x < ld_target_x: 
        right1 = ld_target_x
        left1  = ld_start_x

    ###    tx2 <---> x2
    if rd_start_x > rd_target_x: 
        right2 = rd_start_x  
        left2  = rd_target_x

    ###    x2 <---> tx2
    if rd_start_x < rd_target_x:  
        right2 = rd_target_x
        left2  = rd_start_x

    if right1 > left2:
        return True
    elif right1 < left2:
        return False


def generate_vc(curr1, curr2, targ1, targ2, alt):

    x1 = curr1[0]
    x2 = curr2[0]
    y1 = curr1[1]
    y2 = curr2[1]
    tx1 = targ1[0]
    tx2 = targ2[0]
    ty1 = targ1[1]
    ty2 = targ2[1]

    # calculating dx & dy
    dx1_tx1 = abs(x1-tx1)
    dy1_ty1 = abs(y1-ty1)
    dx2_tx2 = abs(x2-tx2)
    dy2_ty2 = abs(y2-ty2)

    # calculating slopes
    s1 = (dy1_ty1)/ (dx1_tx1)
    s2 = (dy2_ty2)/ (dx2_tx2)

    # initializing constants
    c1=0
    c2=0

    ## check if their slopes are the same or not, if no, that means they might have a crossing point
    if s1 != s2:
        print("Different slopes")
        ## computing the (virual) crossing point 
        c1  = y1-s1*x1
        c2  = y2-s2*x2
        vcx = (c2-c1)/(s1-s2)
        vcy = (c1*s2-c2*s1)/(s2-s1) 

        ## check if this crossing point is in the line segment or not (first we need to make sure the boundaries)
        right1 = 0
        left1  = 0
        right2 = 0
        left2  = 0

        if x1 > tx1:    ###    tx1 <---> x1
            right1 = x1
            left1  = tx1

        if x1 < tx1: ###    x1 <---> tx1
            right1 = tx1
            left1  = x1

        if x2 > tx2:
            right2 = x2  ###    tx2 <---> x2
            left2  = tx2

        if x2 < tx2:  ###    x2 <---> tx2
            right2 = tx2
            left2  = x2

        ## if the crossing point is in the segments, make the crossing point as VC and return it
        if left1 <= vcx and vcx <= right1 and left2 <= vcx and vcx <= right2:
            print("two segmented lines have a crossing point")
            return LocationGlobalRelative(vcx, vcy, alt)
        # ## the crossing point is not in the center, that means we dont need collision avoidance in this case
        else:
            print("No crossing point with two segment lines")
            return -1

    
    ## check if their slope are the same or not, if yes check if they are parallel or overlaps
    elif s1 == s2 and c1 == c2:
        # #check if they are parallel
        # if c1 != c2:
        #     print("they are parallel")

        # ## two lines overlaps
        # elif c1 == c2:
        #     ## midpoint of two drones           
        print("they are overlapped")
        return LocationGlobalRelative((x1+x2)/2, (y1+y2)/2, alt)

    else:
        print("Error")
        return -1

## testing
#print(check_crossingpoint(2,-3,0,0,4,-3,1,1))
# print(generate_vc(0,0,2,3,3,3,4,3))
#print(generate_vc(0,0,2,-3,1,1,4,-3))
# print(generate_vc(0,0, 5,0, 4,0, 2,0))

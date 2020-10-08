
def generate_vc(x1,y1,x2,y2,tx1,ty1,tx2,ty2):
    dx1_tx1 = abs(x1-tx1)
    dy1_ty1 = abs(y1-ty1)
    dx2_tx2 = abs(x2-tx2)
    dy2_ty2 = abs(y2-ty2)

    s1 = (dy1_ty1)/ (dx1_tx1)
    s2 = (dy2_ty2)/ (dx2_tx2)

    c1=0
    c2=0

    if s1 != s2:
        c1 = y1-s1*x1
        c2 = y2-s2*x2
        vcx = (c2-c1)/(s1-s2)
        vcy = (c1*s2-c2*s1)/(s2-s1) 
        return (vcx,vcy)
    #elif s1 == s2:
        ##check if they are parallel
        # if parallel:
        #    do nothing since they wont crash
        # else:
        # return midpoint of two drones ( (x1+x2)/2, (y1+y2)/2 )

print(generate_vc(0,0,2,3,1,1,4,3))
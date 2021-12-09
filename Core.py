#################################################################
#                                                               #
#          CORE 	                                        #
#                        version: null                          #
# @author: Sergio Lins               sergio.lins@roma3.infn.it  #
#################################################################

def plot(image):
    image_norm = image/image.max()*255
    image_color = ImgMath.colorize(image_norm,'green')
    fig, ax = plt.subplots()
    plt.imshow(image_color)
    plt.show()
    return 0

if __name__=="__main__":

    import sys
    import SpecRead
    import ImgMath
    from PyMca5.PyMcaPhysics import Elements
    import matplotlib.pyplot as plt
    import logging

    inputlist = ['-findelement','Core.py','-normalize','-getratios'] 
    elementlist = []
    flag1 = sys.argv[1]
    if flag1 == '-help':
        print("\nUSAGE: '-findelement'; plots a 2D map of elements which are to be set.\
Additionally, you can type '-normalize' when finding one element to generate\
an image where the element is displayed in proportion to the most abundant element.\n\
       '-plotmap'; plots a density map\n\
       '-plotstack'; plots the sum spectra of all sample. Optional: you can add '-semilog' to plot it in semilog mode.\n\
       '-getratios x'; creates the ka/kb or la/lb ratio image for element 'x'. K or L are chosen accordingly.")
    if flag1 == '-findelement':    
        import Mapping
        input_elements = input('Please input which elements are to be mapped (maximum of 3): \n')
        input_elements = input_elements.split(' ')
        for arg in range(len(input_elements)):
            if input_elements[arg] in Elements.ElementList:
                elementlist.append(input_elements[arg])
            else: 
                raise Exception("%s not an element!" % input_elements[arg])
                logging.exception("{0} is not a chemical element!".format(input_elements[arg]))
        
        if '-normalize' in sys.argv:
            for element in elementlist:
                image = Mapping.getpeakmap(element)
                plot(image)
        else:
            for element in elementlist:
                image = Mapping.getpeakmap(element)
                plot(image)

    if flag1 == '-plotmap':
        print("Fetching density map...")
        Mapping.plotdensitymap()
    if flag1 == '-plotstack':
        if len(sys.argv) >= 3:
            flag2 = sys.argv[2]
        else:
            flag2 = None
        SpecMath.getstackplot(SpecRead.getfirstfile(),SpecMath.energyaxis())
    if flag1 == '-getratios':
        for arg in range(len(sys.argv)):
            if sys.argv[arg] in Elements.ElementList:
                elementlist.append(sys.argv[arg])
            else: 
                if sys.argv[arg] in inputlist:
                    pass
                else: 
                    raise Exception("%s not an element!" % sys.argv[arg])
        ratiofile = SpecRead.workpath + '/output/{1}_ratio_{0}.txt'\
                .format(elementlist[0],SpecRead.DIRECTORY)
        ratiomatrix = SpecRead.RatioMatrixReadFile(ratiofile)
        ratiomatrix = SpecRead.RatioMatrixTransform(ratiomatrix)
        plt.imshow(ratiomatrix)
        plt.show()
        heightmap = ImgMath.getheightmap(ratiomatrix,1.52,'AuSheet',elementlist[0])
        plt.imshow(heightmap,cmap='BuGn')
        plt.show()
        ImgMath.plot3D(heightmap)

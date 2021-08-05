#Judith Weng Zhu
#Draws tote and asks for user input

from tkinter.ttk import setup_master
import adsk.core, adsk.fusion, adsk.cam, traceback
from tkinter import *


def bag_pattern(height_patt,width_patt,corner_patt,page,line):
    #draws the bag, straps given dimn and which page to draw on
    base_patt = (width_patt/2) - corner_patt 

    #sketch the points that will make up the lines
    #the values of points are variables, depend on the user's input
    origin = adsk.core.Point3D.create(0,0,0)
    midtop = adsk.core.Point3D.create(0,height_patt,0)
    topcorner = adsk.core.Point3D.create(base_patt,height_patt,0)
    midcorner = adsk.core.Point3D.create(base_patt,height_patt-corner_patt,0)
    sidecorner = adsk.core.Point3D.create(base_patt+corner_patt,height_patt-corner_patt,0)
    bottom = adsk.core.Point3D.create(base_patt+corner_patt,0,0)

    #draw lines
    midline = line.addByTwoPoints(origin, midtop)
    top = line.addByTwoPoints(midline.endSketchPoint, topcorner)
    vcorner = line.addByTwoPoints(top.endSketchPoint, midcorner)
    hcorner = line.addByTwoPoints(vcorner.endSketchPoint, sidecorner)
    edge = line.addByTwoPoints(hcorner.endSketchPoint, bottom)
    base = line.addByTwoPoints(edge.endSketchPoint, midline.startSketchPoint)

    #the midline is not part of pattern
    #it's just a symmetry line
    midline.isConstruction = True 

    #draw the exact same lines
    ntop = line.addByTwoPoints(midline.endSketchPoint, topcorner)
    nvcorner = line.addByTwoPoints(ntop.endSketchPoint, midcorner)
    nhcorner = line.addByTwoPoints(nvcorner.endSketchPoint, sidecorner)
    nedge = line.addByTwoPoints(nhcorner.endSketchPoint, bottom)
    nbase = line.addByTwoPoints(nedge.endSketchPoint, midline.startSketchPoint)

    #then mirror these lines over the symmetry line
    page.geometricConstraints.addSymmetry(top.endSketchPoint, ntop.endSketchPoint, midline)
    page.geometricConstraints.addSymmetry(vcorner.endSketchPoint, nvcorner.endSketchPoint, midline)
    page.geometricConstraints.addSymmetry(hcorner.endSketchPoint, nhcorner.endSketchPoint, midline)
    page.geometricConstraints.addSymmetry(edge.endSketchPoint, nedge.endSketchPoint, midline)
    

    #labels pattern
    # texts = page.sketchTexts
    # input = texts.createInput2('Bag Panel \n(cut 2)', 1.5)
    # input.setAsMultiLine(origin, midcorner,
    #                     adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
    #                     adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    # texts.add(input)


def straps():
    ##########################################################################
    #STRAPS:
    #FIXED MEASUREMENTS
    # straps are 46cm by 7.5cm
    #3cm away from the main pattern

    s_top = adsk.core.Point3D.create(-23,-3,0)
    s_bott = adsk.core.Point3D.create(23,-10.5,0)

    lineOut.addTwoPointRectangle(s_top,s_bott)

    # input = textsOut.createInput2('Straps \n(cut 2)', 1.5)
    # input.setAsMultiLine(s_top,s_bott,
    #                     adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
    #                     adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    # textsOut.add(input)


def outerPocket(height_patt,width_patt,corner_patt):
    ##########################################################################
    #OUTER POCKET 
    #Optional, users should choose whether to include
    #measurements should be variables
    #width is the same as the bag
    #proportional to height
    #about 3.5cm below straps

    pocket_height = 0.7*height_patt
    #pocket_width = width_patt + 2*(corner_patt+seam)  #this is half of the pattern width


    pcorner1 = adsk.core.Point3D.create(width_patt/-2,-14,0)
    pcorner2= adsk.core.Point3D.create(width_patt/2,-14-pocket_height,0)

    lineOut.addTwoPointRectangle(pcorner1,pcorner2)
    


    # input = textsOut.createInput2('Outer Pocket \n(cut 1)', 1.5)
    # input.setAsMultiLine(pcorner1, pcorner2,
    #                     adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
    #                     adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    # textsOut.add(input)



def interiorPocket(height_patt,width_patt,corner_patt):
    ###########################3
    #INTERIOR POCKET
    pocket_width = 0.6*width_patt
    pocket_height = 0.9*height_patt
    lineIn = inner.sketchCurves.sketchLines
    ip_upper = adsk.core.Point3D.create(pocket_width/-2,-3,0)
    ip_lower = adsk.core.Point3D.create(pocket_width/2,-3-pocket_height,0)

    lineIn.addTwoPointRectangle(ip_upper,ip_lower)

def makeform(root, fields):
    #creates the form that lets users input the dimensions
    entries = {}
    for field in fields:
        row = Frame(root) #window container
        lab = Label(row, width=22, text=field+": ", anchor='w')
        ent = Entry(row)

        row.pack(side=TOP, 
                 fill=X, 
                 padx=5, 
                 pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, 
                 expand=YES, 
                 fill=X)
        entries[field] = ent
    #returns inputs
    return entries

def make_pattern(ents,root,var):
    app = adsk.core.Application.get()
    ui  = app.userInterface
    #ui.messageBox('Hello script')

    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType) #creates it in a new doc
    doc.name = "Outer"
    design = app.activeProduct
    rootComp = design.rootComponent
    sketch1 = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane
    unitsMgr = design.fusionUnitsManager
    unitsMgr.distanceDisplayUnits = adsk.fusion.DistanceUnits.InchDistanceUnits

    # height = 27
    # width = 25.5
    # depth=10

    height = (float(ents['Height'].get()))*2.56
    width = (float(ents['Width'].get()))*2.56
    depth = (float(ents['Depth'].get()))*2.56
    global seam 

    #calculate pattern dimensions from input
    seam = 0.635 #this is in cm. equiv to 1/4"
    corner_patt = 0.5*depth + seam   #dimensions of a corner side
    width_patt = width + 2*(seam+corner_patt)  #this is half of the pattern width, shorter side
    height_patt = height + corner_patt


    root.destroy()

    #outer patterns
    global outer,lineOut,textsOut,inner,lineOut,textsOut,extrudes
    extrudes = rootComp.features.extrudeFeatures 

    outer = sketch1.add(xyPlane)
    lineOut = outer.sketchCurves.sketchLines
    textsOut = outer.sketchTexts
    bag_pattern(height_patt,width_patt,corner_patt,outer,lineOut)
    straps()
    #if the checkbox for outter pocket was checked
    if (var.get() == 1):
        outerPocket(height_patt,width_patt,corner_patt)




    #lining
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType) #creates it in a new doc
    doc.name = "Lining"
    design = app.activeProduct
    rootComp = design.rootComponent
    sketch2 = rootComp.sketches 
    unitsMgr = design.fusionUnitsManager
    unitsMgr.distanceDisplayUnits = adsk.fusion.DistanceUnits.InchDistanceUnits

    inner = sketch2.add(xyPlane)
    extrudes2 = rootComp.features.extrudeFeatures 

    lineIn = inner.sketchCurves.sketchLines
    bag_pattern(height_patt,width_patt,corner_patt,inner,lineIn)
    interiorPocket(height_patt,width_patt,corner_patt)

    # Create an object collection to use an input.
    all_profOut = adsk.core.ObjectCollection.create()
    all_profIn = adsk.core.ObjectCollection.create()    \

    # Add all of the profiles to a collection.
    for prof in outer.profiles:
        all_profOut.add(prof)
    for prof in inner.profiles:
        all_profIn.add(prof)


    # create 0.0001 cm thickness
    distance = adsk.core.ValueInput.createByReal(0.0001)
    extrude1 = extrudes.addSimple(all_profOut, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)  
    extrude2 = extrudes2.addSimple(all_profIn, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)  








def run(context):
    ui = None
    try:
        fields = ('Height', 'Width', 'Depth')  #entry fields
        
        root = Tk()
        root.title("Design a tote bag")
        labl = Label(root,text='Enter tote dimensions in inches')
        labl.pack()

        ents = makeform(root, fields) 
        var=IntVar()
        c1 = Checkbutton(root, text='With Outer Pocket',variable=var, onvalue=1, offvalue=0)
        c1.pack()

        b1 = Button(root, text='Design',
            command=lambda:[make_pattern(ents,root,var)]) #button that creates pattern
        b1.pack(side=RIGHT, padx=5, pady=5)

        root.mainloop()


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

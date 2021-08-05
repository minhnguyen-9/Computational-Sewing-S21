#Judith Weng Zhu
#Last edited: August 5, 2021
#Draws pattern provided in tutorial in one function

import adsk.core, adsk.fusion, adsk.cam, traceback
from tkinter import *



def scale(sketchPlane,rootComp,length,width):
    extrudes = rootComp.features.extrudeFeatures
    scales = rootComp.features.scaleFeatures
    # Create an extrusion input

    extInput = extrudes.createInput(sketchPlane.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    
    # Define that the extent is a distance extent of 0.025 cm
    distance = adsk.core.ValueInput.createByReal(0.025)
    extInput.setDistanceExtent(False, distance)

    # Create the extrusion
    ext = extrudes.add(extInput)
    
    # Get the body created by the extrusion
    body = ext.bodies.item(0)
    
    # Create a scale input
    inputColl = adsk.core.ObjectCollection.create()
    inputColl.add(body)

    basePt = sketchPlane.sketchPoints.item(0)        
    scaleFactor = adsk.core.ValueInput.createByReal(1)
    scaleInput = scales.createInput(inputColl, basePt,scaleFactor)
    
    # Set the scale to be non-uniform
    xScale = adsk.core.ValueInput.createByReal(0.0727*width + 0.323) 
    yScale = adsk.core.ValueInput.createByReal(0.0376*length + 0.188)
    zScale = adsk.core.ValueInput.createByReal(1)
    scaleInput.setToNonUniform(xScale, yScale, zScale)
    
    scale = scales.add(scaleInput)



def upper_pattern(upper):  

    lineUp = upper.sketchCurves.sketchLines

    left_base = adsk.core.Point3D.create(0,0,0)
    right_base = adsk.core.Point3D.create(0.1,0,0)

    outer = adsk.core.ObjectCollection.create()
    outerFirst = adsk.core.Point3D.create(-8.553,-1.889,0)
    outerLast = adsk.core.Point3D.create(8.56,-1.788,0)
    outer.add(outerFirst)
    outer.add(adsk.core.Point3D.create(-9.067,8.068,0))
    outer.add(adsk.core.Point3D.create(-6.242,21.738,0))
    outer.add(adsk.core.Point3D.create(0.026,24.807,0))
    outer.add(adsk.core.Point3D.create(6.213,21.525,0))
    outer.add(adsk.core.Point3D.create(8.789,8.068,0))
    outer.add(outerLast)
    
    inner = adsk.core.ObjectCollection.create()
    inner.add(left_base)
    inner.add(adsk.core.Point3D.create(-2,7,0))
    inner.add(adsk.core.Point3D.create(-1.5,10,0))
    inner.add(adsk.core.Point3D.create(-0.1,10.80,0))
    inner.add(adsk.core.Point3D.create(1.269,10.097,0))
    inner.add(adsk.core.Point3D.create(1.49,5.341,0))
    inner.add(right_base)

    upper.sketchCurves.sketchFittedSplines.add(outer)
    upper.sketchCurves.sketchFittedSplines.add(inner)
    lineUp.addByTwoPoints(left_base,outerFirst)
    lineUp.addByTwoPoints(outerLast,right_base) 


def upperFusible(upFusible):
    lineUpFus = upFusible.sketchCurves.sketchLines

    left_base = adsk.core.Point3D.create(0,0,0)
    right_base = adsk.core.Point3D.create(2.66,0,0)

    outer = adsk.core.ObjectCollection.create()
    outerFirst = adsk.core.Point3D.create(-7.379,-1.644,0)
    outerLast = adsk.core.Point3D.create(9.845,	-1.644,0)
    outer.add(outerFirst)
    outer.add(adsk.core.Point3D.create(-7.647,	8.551,0))
    outer.add(adsk.core.Point3D.create(-4.601,	21.554,0))
    outer.add(adsk.core.Point3D.create(1.326,	24.01,0))
    outer.add(adsk.core.Point3D.create(6.916,	21.554,0))
    outer.add(adsk.core.Point3D.create(9.985,	8.531,0))
    outer.add(outerLast)
    
    innerLeft = adsk.core.ObjectCollection.create()
    innerLeft.add(left_base)
    left_in = adsk.core.Point3D.create(0.262,	10.845,0)
    innerLeft.add(adsk.core.Point3D.create(-1.475,	8.531,0))
    innerLeft.add(left_in)

    innerUp = adsk.core.ObjectCollection.create()
    innerUpFirst = adsk.core.Point3D.create(0.269,	16.474,0)
    innerUp.add(innerUpFirst)
    innerUp.add(adsk.core.Point3D.create(0.439,	17.49,0))
    innerUp.add(adsk.core.Point3D.create(1.15,	17.8,0))
    innerUp.add(adsk.core.Point3D.create(1.836,	17.49,0))
    innerUpLast = adsk.core.Point3D.create(2.09,	16.474,0)
    innerUp.add(innerUpLast)


    innerRight = adsk.core.ObjectCollection.create()
    right_in = adsk.core.Point3D.create(2.09,	10.759,0)
    innerRight.add(right_in)
    innerRight.add(adsk.core.Point3D.create(3.729,	8.531,0))
    innerRight.add(right_base)


    upFusible.sketchCurves.sketchFittedSplines.add(outer)
    upFusible.sketchCurves.sketchFittedSplines.add(innerLeft)
    upFusible.sketchCurves.sketchFittedSplines.add(innerUp)
    upFusible.sketchCurves.sketchFittedSplines.add(innerRight)
    lineUpFus.addByTwoPoints(left_base,outerFirst)
    lineUpFus.addByTwoPoints(outerLast,right_base) 
    lineUpFus.addByTwoPoints(innerUpFirst,left_in)
    lineUpFus.addByTwoPoints(right_in,innerUpLast)  

def sole(sketchSole):
    lineSole = sketchSole.sketchCurves.sketchLines

    origin = adsk.core.Point3D.create(0,-3,0)  #translated -3 units to leave space for upper
    first = adsk.core.Point3D.create(0.747,-3.81,0)
    last = adsk.core.Point3D.create(-0.753,-3.81,0)

    outer = adsk.core.ObjectCollection.create()
    outer.add(first)
    outer.add(adsk.core.Point3D.create(2.95,-4.72,0))
    outer.add(adsk.core.Point3D.create(4.089,-7.586,0))
    outer.add(adsk.core.Point3D.create(5.157,-14.848,0))
    outer.add(adsk.core.Point3D.create(5.638,-23.607,0))
    outer.add(adsk.core.Point3D.create(4.605,-26.846,0))
    outer.add(adsk.core.Point3D.create(0.849,-29.089,0))
    outer.add(adsk.core.Point3D.create(-2.248,-28.929,0))
    outer.add(adsk.core.Point3D.create(-4.402,-27.096,0))
    outer.add(adsk.core.Point3D.create(-4.653,-21.81,0))
    outer.add(adsk.core.Point3D.create(-4.044,-16.385,0))
    outer.add(adsk.core.Point3D.create(-3.553,-8.41,0))
    outer.add(adsk.core.Point3D.create(-3.055,-5.371,0))
    outer.add(last)

    sketchSole.sketchCurves.sketchFittedSplines.add(outer)
    lineSole.addByTwoPoints(origin,first)
    lineSole.addByTwoPoints(origin,last)

def soleFusible(sketchSoleFus):

    outer = adsk.core.ObjectCollection.create()
    start = adsk.core.Point3D.create(0,-3,0)
    outer.add(start)
    outer.add(adsk.core.Point3D.create(1.921,-3.779,0))
    outer.add(adsk.core.Point3D.create(3.291,-8.378,0))
    outer.add(adsk.core.Point3D.create(3.65,-13.467,0))
    outer.add(adsk.core.Point3D.create(4.367,-17.968,0))
    outer.add(adsk.core.Point3D.create(4.367,-22.959,0))
    outer.add(adsk.core.Point3D.create(1.97,-26.35,0))
    outer.add(adsk.core.Point3D.create(-.23,-26.95,0))
    outer.add(adsk.core.Point3D.create(-2.269,-26.347,0))
    outer.add(adsk.core.Point3D.create(-3.963,-23.916,0))
    outer.add(adsk.core.Point3D.create(-3.93,-19.15,0))
    outer.add(adsk.core.Point3D.create(-3.217,-15.459,0))
    outer.add(adsk.core.Point3D.create(-2.814,-7.673,0))
    outer.add(adsk.core.Point3D.create(-2.335,-4.951,0))
    outer.add(start)

    sketchSoleFus.sketchCurves.sketchFittedSplines.add(outer)



def pattern(ents,root):
    length = (float(ents['Length'].get()))*2.56  #convert input to cm
    width = (float(ents['Width'].get()))*2.56

    app = adsk.core.Application.get()
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType) #creates it in a new doc
    doc.name = "Shoe Pattern Outer"
    design = app.activeProduct
    rootComp = design.rootComponent

    sketch1 = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane  
    upper = sketch1.add(xyPlane)
    upper.name = 'Upper Shoe Pattern'
    upper_pattern(upper)
    scale(upper,rootComp,length,width)

    sketchSole = sketch1.add(xyPlane)
    sketchSole.name = "Shoe Sole Pattern"
    sole(sketchSole)
    scale(sketchSole,rootComp,length,width)


    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType) #creates it in a new doc
    doc.name = "Shoe Pattern Fusible"
    design = app.activeProduct
    rootComp = design.rootComponent

    sketch2 = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane  
    upFusible = sketch2.add(xyPlane)
    upFusible.name = 'Upper Shoe Pattern'
    upperFusible(upFusible)
    scale(upFusible,rootComp,length,width)

    sketchSoleFus = sketch2.add(xyPlane)
    sketchSoleFus.name = "Shoe Sole Pattern"
    soleFusible(sketchSoleFus)
    scale(sketchSoleFus,rootComp,length,width)

    root.destroy()


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



def run(context):
    ui = None
    try:
        #ui  = app.userInterface
        fields = ('Length', 'Width')  #entry fields
        
        root = Tk()
        root.title("Customize your shoes!")
        labl = Label(root,text="Enter your foot's dimensions in inches")
        labl.pack()

        ents = makeform(root, fields) 

        b1 = Button(root, text='Design',
            command=lambda:[pattern(ents,root)]) #button that creates pattern
        b1.pack(side=RIGHT, padx=5, pady=5)

        root.mainloop()






    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))






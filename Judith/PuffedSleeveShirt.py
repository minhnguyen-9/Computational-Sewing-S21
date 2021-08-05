#Judith Weng Zhu
#Last edited: July 27, 2021
# https://www.youtube.com/watch?v=ek7G-rCMeoo tutorial

import adsk.core, adsk.fusion, adsk.cam, traceback
from tkinter import *


def make_sleeves(sleeve,lineSleeve,arm,shoulder):

    hcorner = 0.5*(shoulder-1)
    width = 2*(10+arm+hcorner) 
    height = width*0.5 

    #sketch the points that will make up the lines
    #the values of points are variables, depend on the user's input
    origin = adsk.core.Point3D.create(0,0,0)
    midtop = adsk.core.Point3D.create(0,height,0)  #height of sleeve
    topcorner = adsk.core.Point3D.create(0.5*width-hcorner,height,0)
    sidecorner = adsk.core.Point3D.create(0.5*width,height-shoulder,0)
    bottom = adsk.core.Point3D.create(0.5*width,0,0)

    #draw lines
    midline = lineSleeve.addByTwoPoints(origin, midtop)
    top = lineSleeve.addByTwoPoints(midline.endSketchPoint, topcorner)
    corner = lineSleeve.addByTwoPoints(top.endSketchPoint, sidecorner)
    edge = lineSleeve.addByTwoPoints(corner.endSketchPoint, bottom)
    base = lineSleeve.addByTwoPoints(edge.endSketchPoint, midline.startSketchPoint)

    #the midline is not part of pattern
    #it's just a symmetry line
    midline.isConstruction = True 

    #draw the exact same lines
    ntop = lineSleeve.addByTwoPoints(midline.endSketchPoint, topcorner)
    ncorner = lineSleeve.addByTwoPoints(ntop.endSketchPoint, sidecorner)
    nedge = lineSleeve.addByTwoPoints(ncorner.endSketchPoint, bottom)
    nbase = lineSleeve.addByTwoPoints(nedge.endSketchPoint, midline.startSketchPoint)

    #then mirror these lines over the symmetry line
    sleeve.geometricConstraints.addSymmetry(top.endSketchPoint, ntop.endSketchPoint, midline)
    sleeve.geometricConstraints.addSymmetry(corner.endSketchPoint, ncorner.endSketchPoint, midline)
    sleeve.geometricConstraints.addSymmetry(edge.endSketchPoint, nedge.endSketchPoint, midline)

    #########################################################################
    #sleeve strap

    sl_top = adsk.core.Point3D.create(-0.5*width,-4,0) #same width as sleeve and 4cm height
    sl_bott = adsk.core.Point3D.create(0.5*width,0,0)  #same as bottom point

    lineSleeve.addTwoPointRectangle(sl_top,sl_bott)


def make_bodice(bodice,lineBodice,lineStrap,bust,shoulder,body):
   
    ##########################################################################

    #Waist strap
    width = 1.85*bust
    s_top = adsk.core.Point3D.create(-0.5*width,-4,0)
    s_bott = adsk.core.Point3D.create(0.5*width,-12,0)

    lineStrap.addTwoPointRectangle(s_top,s_bott) #use where sleeve left off


    ############    
    #Bodice

    height = body + 4
    width = 0.75*bust
    vcorner = 0.5*(shoulder-1)  #shoulder is now howizontal corner distance for bodice

    midbottom = adsk.core.Point3D.create(0,-12,0) #origin - 12j
    midtop = adsk.core.Point3D.create(0,-12-height,0) #upper to under breast - 12j
    topcorner = adsk.core.Point3D.create(0.5*width-shoulder,-12-height,0)
    sidecorner = adsk.core.Point3D.create(0.5*width,vcorner-height-12,0) #upper to under breast - 6j
    bottom = adsk.core.Point3D.create(0.5*width,-12,0)  #bottom - 12j

    arcBodice = bodice.sketchCurves.sketchArcs

    #draw lines
    midline = lineBodice.addByTwoPoints(midbottom, midtop)
    corner = lineBodice.addByTwoPoints(topcorner, sidecorner)
    edge = lineBodice.addByTwoPoints(corner.endSketchPoint, bottom)

    #the midline is not part of pattern
    #it's just a symmetry line
    midline.isConstruction = True 

    # #draw the exact same lines
    ncorner = lineBodice.addByTwoPoints(topcorner, sidecorner)
    nedge = lineBodice.addByTwoPoints(ncorner.endSketchPoint, bottom)

    # #then mirror these lines over the symmetry line
    bodice.geometricConstraints.addSymmetry(corner.startSketchPoint, ncorner.startSketchPoint, midline)
    bodice.geometricConstraints.addSymmetry(corner.endSketchPoint, ncorner.endSketchPoint, midline)
    bodice.geometricConstraints.addSymmetry(edge.endSketchPoint, nedge.endSketchPoint, midline)

    lowNeck = adsk.core.Point3D.create(0,-height-12+(0.5*vcorner),0)
    highWaist = adsk.core.Point3D.create(0,-16,0)
    # #draw arcs
    # #try to do find a way to translate points if its easier
    arcBodice.addByThreePoints(topcorner,lowNeck,ncorner.startSketchPoint) #neck
    arcBodice.addByThreePoints(bottom,highWaist,nedge.endSketchPoint) #waist
    


def make_pattern(ents,root):
    app = adsk.core.Application.get()
    ui  = app.userInterface


    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType) #creates it in a new doc
    doc.name = "Puff Sleeve Shirt"
    design = app.activeProduct
    rootComp = design.rootComponent
    xyPlane = rootComp.xYConstructionPlane  

    unitsMgr = design.fusionUnitsManager
    unitsMgr.distanceDisplayUnits = adsk.fusion.DistanceUnits.InchDistanceUnits

    sketch = rootComp.sketches
    sleeve = sketch.add(xyPlane)
    lineSleeve = sleeve.sketchCurves.sketchLines
    sleeve.name = "Sleeves Pattern"
    bodice = sketch.add(xyPlane)
    bodice.name = "Bodice Pattern"
    lineBodice = bodice.sketchCurves.sketchLines
    waist = sketch.add(xyPlane)
    waist.name = "Waist Strap"
    lineWaist = waist.sketchCurves.sketchLines


    arm = (float(ents['Arm Circumference'].get()))*2.56 #convert from inches to cm
    bust = (float(ents['Bust'].get()))*2.56  #convert from inches to cm
    shoulder = (float(ents['Shoulder to Upper Breast'].get()))*2.56
    body = (float(ents['Upper to Under Breast'].get()))*2.56

    root.destroy() #close window
    # arm = 24  #9.375in
    # bust = 81+(1/3)  #31.77in
    # shoulder =13 #5.078in
    # body = 20 #7.8125in

    make_sleeves(sleeve,lineSleeve,arm,shoulder)
    make_bodice(bodice,lineBodice,lineWaist,bust,shoulder,body)


    extrudes = rootComp.features.extrudeFeatures 

    # create 0.025 cm thickness
    distance = adsk.core.ValueInput.createByReal(0.025)
    extrudes.addSimple(sleeve.profiles.item(0), distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)  
    extrudes.addSimple(sleeve.profiles.item(1), distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)  
    extrudes.addSimple(bodice.profiles.item(0), distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)  
    extrudes.addSimple(waist.profiles.item(0), distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)  


def makeform(root, fields):
    #creates the form that lets users input the dimensions
    entries = {}
    for field in fields:
        row = Frame(root) #window container
        lab = Label(row, width=30, text=field+": ", anchor='w')
        ent = Entry(row)

        row.pack(side=TOP, 
                 fill=X, 
                 padx=25, 
                 pady=10)
        lab.pack(side=LEFT)
        ent.pack()
        ent.place(x=180)
        entries[field] = ent
    #returns inputs
    return entries



def run(context):
    ui = None
    try:
        fields = ('Arm Circumference','Bust','Shoulder to Upper Breast','Upper to Under Breast')  #entry fields
        
        root = Tk()
        root.title("Design a puffed sleeve shirt")
        labl = Label(root,text='Enter measurements in inches')
        labl.pack()

        ents = makeform(root, fields) 

        b1 = Button(root, text='Design',
            command=lambda:[make_pattern(ents,root)]) #button that creates pattern
        b1.pack(side=RIGHT, padx=5, pady=5)

        root.mainloop()





    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))






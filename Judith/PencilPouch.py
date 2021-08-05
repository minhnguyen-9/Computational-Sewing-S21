# Judith Weng Zhu - Last Updated 6/29
# This code asks for user inputs of a pencil pouch and outputs the pattern
# reference: https://www.python-course.eu/tkinter_entry_widgets.php


import adsk.core, adsk.fusion, adsk.cam, traceback
from tkinter import *

fields = ('Length', 'Width', 'Depth')  #entry fields
app = adsk.core.Application.get()
ui  = app.userInterface
design = app.activeProduct
rootComp = design.rootComponent
sketches = rootComp.sketches


#calculates pattern measurements and draws them on fusion 360
def make_pattern(entries,root):
    #convert to pattern measurements
    len = float(entries['Length'].get())
    width = float(entries['Width'].get())
    depth = float(entries['Depth'].get()) 

    #calculate inputs into outputs and convert into cm
    patternLen = (0.6847*len + 1.1669*depth)*2.56
    patternWid = (0.7273*width + 1.8182*depth)*2.56


    xyPlane = rootComp.xYConstructionPlane  
    xy = sketches.add(xyPlane)
    lines = xy.sketchCurves.sketchLines


    #create rectangle
    point1 = adsk.core.Point3D.create(0, 0, 0)
    point2 = adsk.core.Point3D.create(patternLen, patternWid, 0) #this is in cm
    recLines = lines.addTwoPointRectangle(point1,point2)

    point3 = adsk.core.Point3D.create(-3, 0, 0)
    reflectLen = -3-patternLen
    point4 = adsk.core.Point3D.create(reflectLen, patternWid, 0) #this is in cm
    recLines2 = lines.addTwoPointRectangle(point3,point4)

    # Get the SketchTexts collection object.
    texts = xy.sketchTexts

    # Add multi-line text.
    input = texts.createInput2('Exterior \n(cut 2)', 1.5)
    input.setAsMultiLine(point1, point2,
                            adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
                            adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    texts.add(input)

    input2 = texts.createInput2('Lining \n(cut 2)', 1.5)
    input2.setAsMultiLine(point3, point4,
                            adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
                            adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    texts.add(input2)

    #close the window
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
    return entries




def run(context):

    try:
            #this just displays the measurements
        unitsMgr = design.fusionUnitsManager
        unitsMgr.distanceDisplayUnits = adsk.fusion.DistanceUnits.InchDistanceUnits #display in inches
        
        root = Tk()
        labl = Label(root,text='Enter pouch dimensions')
        labl.pack()

        ents = makeform(root, fields)
        b1 = Button(root, text='Design',
            command=lambda:[make_pattern(ents,root)]) #button that creates pattern
        b1.pack(side=RIGHT, padx=5, pady=5)


        root.mainloop()


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
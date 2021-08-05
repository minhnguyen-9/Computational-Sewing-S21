#Author-Minh Nguyen
#Description-Making a box t-shirt 


import adsk.core, adsk.fusion, adsk.cam, traceback
import math

app = None
ui  = None
commandId = 't-shirt'
commandName = 'Box t-shirt'
commandDescription = 'To make a t-shirt'

# Global set of event handlers to keep them referenced for the duration of the command
handlers = []

class MyCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            command = args.firingEvent.sender
            inputs = command.commandInputs

            # We need access to the inputs within a command during the execute.
            tabCmdInput1 = inputs.itemById(commandId + '_tab_1')
            tab1ChildInputs = tabCmdInput1.children
            
            design = app.activeProduct
            rootComp = design.rootComponent
            # Create a new sketch on the xy plane.	
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)

            inch = 2.54
            sign = 1 ## just incase that we need to mirror the design
 
            ########### Top piece construction ################
            front_1 = adsk.core.ObjectCollection.create()
            front_2 = adsk.core.ObjectCollection.create()
            front_3 = adsk.core.ObjectCollection.create()
            
            back_1 = adsk.core.ObjectCollection.create()
            back_2 = adsk.core.ObjectCollection.create()
            back_3 = adsk.core.ObjectCollection.create()

   
            
            front_1.add(adsk.core.Point3D.create(11.23*(inch*sign), 0, 0))
            front_1.add(adsk.core.Point3D.create(11.20*(inch*sign), 0.625*(inch*sign), 0))
            front_1.add(adsk.core.Point3D.create(11*(inch*sign), 8.45*(inch*sign), 0))
            front_1.add(adsk.core.Point3D.create(10.875*(inch*sign), 13.30*(inch*sign), 0))
            front_1.add(adsk.core.Point3D.create(11.125*(inch*sign),16.5*(inch*sign), 0))
            front_1.add(adsk.core.Point3D.create(11.25*(inch*sign),17.125*(inch*sign) , 0))
            #front_1.add(adsk.core.Point3D.create( front_end_1_x, front_end_1_y , 0))

    
            front_2.add(adsk.core.Point3D.create(11.25*(inch*sign), 17.125*(inch*sign), 0))
            front_2.add(adsk.core.Point3D.create(10.375*(inch*sign), 17.625*(inch*sign), 0))
            front_2.add(adsk.core.Point3D.create(9.50*(inch*sign), 19.125*(inch*sign), 0))
            front_2.add(adsk.core.Point3D.create(9.375*(inch*sign), 20.5*(inch*sign), 0))
            front_2.add(adsk.core.Point3D.create(9.5*(inch*sign), 22.80*(inch*sign), 0))
            front_2.add(adsk.core.Point3D.create(9.875*(inch*sign), 24.81*(inch*sign), 0))
            front_2.add(adsk.core.Point3D.create(10.25*(inch*sign), 26.06*(inch*sign), 0))
            #front_2.add(adsk.core.Point3D.create front_end_2_x,    front_end_2_y, 0))

            front_3.add(adsk.core.Point3D.create(0, 23*(inch*sign), 0))
            front_3.add(adsk.core.Point3D.create(1.5*(inch*sign), 23.875*(inch*sign), 0))
            front_3.add(adsk.core.Point3D.create(2.375*(inch*sign), 25.05*(inch*sign), 0))
            front_3.add(adsk.core.Point3D.create(2.75*(inch*sign), 26.50*(inch*sign), 0))
            front_3.add(adsk.core.Point3D.create(2.75*(inch*sign), 27.55*(inch*sign), 0))

            
            # Create the spline for the top piece.
            front_spline1 = sketch.sketchCurves.sketchFittedSplines.add(front_1)
            front_spline2 = sketch.sketchCurves.sketchFittedSplines.add(front_2)
            front_spline3 = sketch.sketchCurves.sketchFittedSplines.add(front_3)


            # Connect the two splines
            front_lines = sketch.sketchCurves.sketchLines
            front_line_1 = front_lines.addByTwoPoints(front_spline2.endSketchPoint, front_spline3.endSketchPoint)
            front_line_2 = front_lines.addByTwoPoints(front_spline1.startSketchPoint, adsk.core.Point3D.create(0, 0, 0))

            ########### Middle piece construction ################

            back_1 = adsk.core.ObjectCollection.create()
            back_2 = adsk.core.ObjectCollection.create()
            back_3 = adsk.core.ObjectCollection.create()

            offset = 35*inch

            back_1.add(adsk.core.Point3D.create(11.45*(inch*sign)+offset, 0, 0)) #####
            back_1.add(adsk.core.Point3D.create(11.375*(inch*sign)+offset, 5.180*(inch*sign), 0))
            back_1.add(adsk.core.Point3D.create(11.19*(inch*sign)+offset, 11.375*(inch*sign), 0))
            back_1.add(adsk.core.Point3D.create(11.26*(inch*sign)+offset, 14.625*(inch*sign), 0))
            back_1.add(adsk.core.Point3D.create(11.80*(inch*sign)+offset, 16.70*(inch*sign), 0))
            # back_1.add(adsk.core.Point3D.create(back_end_1_x, back_end_1_y, 0))

            back_2.add(adsk.core.Point3D.create(11.80*(inch*sign)+offset, 16.70*(inch*sign), 0))
            back_2.add(adsk.core.Point3D.create(10.25*(inch*sign)+offset, 18.75*(inch*sign), 0))
            back_2.add(adsk.core.Point3D.create(9.615*(inch*sign)+offset, 21.875*(inch*sign), 0))
            back_2.add(adsk.core.Point3D.create(9.75*(inch*sign)+offset, 22.875*(inch*sign), 0))
            back_2.add(adsk.core.Point3D.create(10*(inch*sign)+offset, 24.25*(inch*sign), 0))
            back_2.add(adsk.core.Point3D.create(10.375*(inch*sign)+offset, 25.95*(inch*sign), 0))
            # back_2.add(adsk.core.Point3D.create(back_end_2_x, back_end_2_y, 0))
            
            back_3.add(adsk.core.Point3D.create(3.5*(inch*sign)+offset, 27.75*(inch*sign), 0))
            back_3.add(adsk.core.Point3D.create(2*(inch*sign)+offset, 27.375*(inch*sign), 0))
            back_3.add(adsk.core.Point3D.create(0*(inch*sign)+offset, 27*(inch*sign), 0))

            
            # Create the spline for the middle piece.
            back_spline1 = sketch.sketchCurves.sketchFittedSplines.add(back_1)
            back_spline2 = sketch.sketchCurves.sketchFittedSplines.add(back_2)
            back_spline3 = sketch.sketchCurves.sketchFittedSplines.add(back_3)
            
            # Connect the two splines
            back_lines = sketch.sketchCurves.sketchLines
            back_line_1 = back_lines.addByTwoPoints(back_spline2.endSketchPoint, back_spline3.startSketchPoint)
            back_line_2 = back_lines.addByTwoPoints(back_spline1.startSketchPoint, adsk.core.Point3D.create(0+offset, 0, 0))

            # ####### Arm piece construction ###########

            sign  = 1
            offset = 50*inch

            arm_1 = adsk.core.ObjectCollection.create()
            arm_2 = adsk.core.ObjectCollection.create()
            arm_3 = adsk.core.ObjectCollection.create()

            arm_1.add(adsk.core.Point3D.create(0*(inch*sign)+offset, 0*inch, 0))
            arm_1.add(adsk.core.Point3D.create(0.25*(inch*sign)+offset, 3.375*inch, 0))
            arm_1.add(adsk.core.Point3D.create(0.375*(inch*sign)+offset, 5.80*inch, 0))
            arm_1.add(adsk.core.Point3D.create(0.5*(inch*sign)+offset, 7.8*inch, 0))

            arm_2.add(adsk.core.Point3D.create(0.5*(inch*sign)+offset, 7.8*inch, 0))
            arm_2.add(adsk.core.Point3D.create(2.5*(inch*sign)+offset, 8.26*inch, 0))
            arm_2.add(adsk.core.Point3D.create(4.25*(inch*sign)+offset, 8.83*inch, 0))
            arm_2.add(adsk.core.Point3D.create(6.5*(inch*sign)+offset, 9.75*inch, 0))
            arm_2.add(adsk.core.Point3D.create(7.76*(inch*sign)+offset, 10.27*inch, 0))

            arm_3.add(adsk.core.Point3D.create(7.76*(inch*sign)+offset, 10.27*inch, 0))
            arm_3.add(adsk.core.Point3D.create(8*(inch*sign)+offset, 9.71*inch, 0))
            arm_3.add(adsk.core.Point3D.create(8.625*(inch*sign)+offset, 7.81*inch, 0))
            arm_3.add(adsk.core.Point3D.create(9*(inch*sign)+offset, 6.75*inch, 0))
            arm_3.add(adsk.core.Point3D.create(9.5*(inch*sign)+offset, 5.05*inch, 0))
            arm_3.add(adsk.core.Point3D.create(9.75*(inch*sign)+offset, 4.23*inch, 0))
            arm_3.add(adsk.core.Point3D.create(10*(inch*sign)+offset, 2.9*inch, 0))
            arm_3.add(adsk.core.Point3D.create(10.25*(inch*sign)+offset, 2.22*inch, 0))
            arm_3.add(adsk.core.Point3D.create(10.70*(inch*sign)+offset, 0*inch, 0))

            arm_spline1 = sketch.sketchCurves.sketchFittedSplines.add(arm_1)
            arm_spline2 = sketch.sketchCurves.sketchFittedSplines.add(arm_2)
            arm_spline3 = sketch.sketchCurves.sketchFittedSplines.add(arm_3)



        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
                        
class MyCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # When the command is done, terminate the script
            # This will release all globals which will remove all event handlers      

            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
                
                
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            cmd = args.command
            
            onExecute = MyCommandExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)
            
            onDestroy = MyCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            # Keep the handler referenced beyond this function
            handlers.append(onDestroy)
            inputs = cmd.commandInputs
            global commandId

            design = adsk.fusion.Design.cast(app.activeProduct)
            unitsMgr = design.fusionUnitsManager
            unitsMgr.distanceDisplayUnits = adsk.fusion.DistanceUnits.InchDistanceUnits


            
            # Create tab input 1
            tabCmdInput1 = inputs.addTabCommandInput(commandId + '_tab_1', 'Input measurements')
            tab1ChildInputs = tabCmdInput1.children
            
            # Create string value input
            input1 = tab1ChildInputs.addStringValueInput(commandId + '_string', 'New Letter:', '')


            #Get size of t-shirt
            floatSlider = tab1ChildInputs.addFloatSliderCommandInput('size', 'Pick your size', 'cm', 0, 1.89, False)
            floatSlider.setText('Small','Large')
            
            
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
                
def run(context):
    try:
        global app
        app = adsk.core.Application.get()
        global ui
        ui = app.userInterface

        global commandId
        global commandName
        global commandDescription
        
        # Create command defintion
        cmdDef = ui.commandDefinitions.itemById(commandId)
        if not cmdDef:
            cmdDef = ui.commandDefinitions.addButtonDefinition(commandId, commandName, commandDescription)
            
        # Add command created event
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        # Keep the handler referenced beyond this function
        handlers.append(onCommandCreated)

        # Execute command
        cmdDef.execute()            

        # Prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
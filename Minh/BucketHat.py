#Author-Minh Nguyen
#Description-Program split out 3 sizes of a bucket hat

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

app = None
ui  = None
commandId = 'DialogTextChange'
commandName = 'Make your bucket hat'
commandDescription = 'Make it easy to design a bucket hat'

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

            input1 = tab1ChildInputs.itemById(commandId + '_string')
            size_input = tab1ChildInputs.itemById('size')
            
            design = app.activeProduct
            rootComp = design.rootComponent
            # Create a new sketch on the xy plane.	
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)

            size_value = size_input.expressionOne
            size_value = size_value.strip(' cm')
            size_value = float(size_value)
            correct_size = 1.89-size_value

            
            ########### Top piece construction ################
            piece1_left = adsk.core.ObjectCollection.create()
            piece1_right = adsk.core.ObjectCollection.create()
            # For the left: 16.02 and 31.704 is the cordinate for the largest size, 1.932 and 0.517 is the x-y distance from the largest size
            #    to the second to last point. 14.98 is the angle of the triangle, and 1.999 is the diangonal distance from the 
            #    the largest size to the second to last point 
            # Similar concept for the right 
            piece1_end_left_x = 16.02-(1.932-(math.cos(math.radians(14.98))*(1.999-correct_size))) #minus to shorten the x axis
            piece1_end_left_y = 31.704+ (0.517 - (math.sin(math.radians(14.98))*(1.999-correct_size))) #plus to shorten the y cord-curvature
            piece1_end_right_x = 18.042 - (2.583-(math.cos(math.radians(8.716))*(2.6131-correct_size)))
            piece1_end_right_y = 42.343 + (0.396 - (math.sin(math.radians(8.716))*(2.6131-correct_size)))
            
            

            # piece one left/bottom side
            piece1_left.add(adsk.core.Point3D.create(1.244, 32.971, 0))
            piece1_left.add(adsk.core.Point3D.create(2.314, 33.099, 0))
            piece1_left.add(adsk.core.Point3D.create(4.787, 33.057, 0))
            piece1_left.add(adsk.core.Point3D.create(7.261, 33.015, 0))
            piece1_left.add(adsk.core.Point3D.create(9.901,32.823 , 0))
            piece1_left.add(adsk.core.Point3D.create(12.104,32.546 , 0))
            piece1_left.add(adsk.core.Point3D.create(14.088,32.221 , 0))
            #piece1_left.add(adsk.core.Point3D.create(16.02,31.704 , 0)) ## referencing to the large size cordinate
            piece1_left.add(adsk.core.Point3D.create( piece1_end_left_x, piece1_end_left_y , 0))

            # piece 1 right/top side
            piece1_right.add(adsk.core.Point3D.create(1.283, 43.935, 0))
            piece1_right.add(adsk.core.Point3D.create(5.406, 43.865, 0))
            piece1_right.add(adsk.core.Point3D.create(8.652, 43.617, 0))
            piece1_right.add(adsk.core.Point3D.create(11.267, 43.33, 0))
            piece1_right.add(adsk.core.Point3D.create(15.459, 42.739, 0))
            #piece1_right.add(adsk.core.Point3D.create(18.042, 42.343, 0)) ## referencing to the large size cordinate
            piece1_right.add(adsk.core.Point3D.create(piece1_end_right_x, piece1_end_right_y, 0))

            
            # Create the spline for the top piece.
            spline1_left = sketch.sketchCurves.sketchFittedSplines.add(piece1_left)
            spline1_right = sketch.sketchCurves.sketchFittedSplines.add(piece1_right)

            # Connect the two splines
            lines1 = sketch.sketchCurves.sketchLines
            line1_1 = lines1.addByTwoPoints(spline1_left.startSketchPoint, spline1_right.startSketchPoint)
            line1_2 = lines1.addByTwoPoints(spline1_left.endSketchPoint, spline1_right.endSketchPoint)
        
            ########### Middle piece construction ################

            piece2_left = adsk.core.ObjectCollection.create()
            piece2_right = adsk.core.ObjectCollection.create()

            piece2_end_left_x = 14.784-(1.509-(math.cos(math.radians(50.244))*(2.35959-correct_size))) #minus to shorten the x axis
            piece2_end_left_y = 16.856+ (1.814 - (math.sin(math.radians(50.244))*(2.35959-correct_size))) #plus to shorten the y cord-curvature
            piece2_end_right_x = 20.814 - (1.401-(math.cos(math.radians(54.290))*(2.4003-correct_size)))
            piece2_end_right_y = 21.283 + (1.949 - (math.sin(math.radians(54.290))*(2.4003-correct_size)))

            # piece two left/bottom side
            piece2_left.add(adsk.core.Point3D.create(1.184, 24.067, 0))
            piece2_left.add(adsk.core.Point3D.create(6.12, 23.273, 0))
            piece2_left.add(adsk.core.Point3D.create(10.497, 21.129, 0))
            piece2_left.add(adsk.core.Point3D.create(13.275, 18.67, 0))
            #piece2_left.add(adsk.core.Point3D.create(14.784, 16.856, 0)) ## referencing to the large size cordinate
            piece2_left.add(adsk.core.Point3D.create(piece2_end_left_x, piece2_end_left_y, 0))

            # piece two right/top side
            piece2_right.add(adsk.core.Point3D.create(1.181, 31.628, 0))
            piece2_right.add(adsk.core.Point3D.create(5.546, 31.196, 0))
            piece2_right.add(adsk.core.Point3D.create(8.192, 30.705, 0))
            piece2_right.add(adsk.core.Point3D.create(10.52, 29.97, 0))
            piece2_right.add(adsk.core.Point3D.create(13.579, 28.284, 0))
            piece2_right.add(adsk.core.Point3D.create(15.796, 26.708, 0))
            piece2_right.add(adsk.core.Point3D.create(17.453, 25.206, 0))
            piece2_right.add(adsk.core.Point3D.create(19.413, 23.232, 0))
            #piece2_right.add(adsk.core.Point3D.create(20.814, 21.283, 0)) ## referencing to the large size cordinate
            piece2_right.add(adsk.core.Point3D.create(piece2_end_right_x, piece2_end_right_y, 0))
            

            
            # Create the spline for the middle piece.
            spline2_left = sketch.sketchCurves.sketchFittedSplines.add(piece2_left)
            spline2_right = sketch.sketchCurves.sketchFittedSplines.add(piece2_right)
            
            # Connect the two splines
            lines2 = sketch.sketchCurves.sketchLines
            line2_1 = lines2.addByTwoPoints(spline2_left.startSketchPoint, spline2_right.startSketchPoint)
            line2_2 = lines1.addByTwoPoints(spline2_left.endSketchPoint, spline2_right.endSketchPoint)

            ####### Bottom piece construction ###########
            circle = sketch.sketchCurves.sketchCircles
            stationaryPoint_forCircle = adsk.core.Point3D.create(1.224, 22.931, 0)
            movingPoint_forCircle = adsk.core.Point3D.create(1.224, 2.931+(correct_size), 0) # plus size here is because the y axis would move up
            sketchCircle = circle.addByTwoPoints(stationaryPoint_forCircle, movingPoint_forCircle)
            lines3 = sketch.sketchCurves.sketchLines
            line3_1 = lines3.addByTwoPoints(stationaryPoint_forCircle, movingPoint_forCircle)




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
            
            # Create tab input 1
            tabCmdInput1 = inputs.addTabCommandInput(commandId + '_tab_1', 'Input measurements')
            tab1ChildInputs = tabCmdInput1.children

            # Create string value output
            tab1ChildInputs.addTextBoxCommandInput('readonly_textBox', 'Instruction', 'Please use the slider to make your hat. X-small is 21" and Large is 24" head circumference. <br /> Medium is recommended for any adult', 8, True)

            #Get size of bucket hat
            floatSlider = tab1ChildInputs.addFloatSliderCommandInput('size', 'Pick your size', 'cm', 0, 1.89, False)
            floatSlider.setText('X-small','Large')
            
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

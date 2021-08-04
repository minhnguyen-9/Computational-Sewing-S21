#Author-Michelle
#Description-Halter Top sewing pattern

import adsk.core, adsk.fusion, adsk.cam, traceback

app = adsk.core.Application.get()
ui  = app.userInterface
design = app.activeProduct
rootComp = design.rootComponent 
sketches = rootComp.sketches
handlers = [] # Global set of event handlers to keep them referenced for the duration of the command
commandId = 'cmdInput'
commandName = 'Halter Top'
commandDescription = 'Script to create a halter top pattern.'

class MyCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # We need access to the inputs within a command during the execute.
            command = args.firingEvent.sender
            inputs = command.commandInputs

            tabCmdInput1 = inputs.itemById(commandId + 'tab_1')
            tab1ChildInputs = tabCmdInput1.children
            Length = tab1ChildInputs.itemById(commandId + 'l')
            Width = tab1ChildInputs.itemById(commandId + 'w')

            bust = float(Length.value)
            upperBust = float(Width.value)
            cupSize = (upperBust - bust) - 1

            # Create an object collection for the points.
            cupPoints = adsk.core.ObjectCollection.create()
            splinePoints = adsk.core.ObjectCollection.create()
            splinePoints2 = adsk.core.ObjectCollection.create()
            bodicePoints = adsk.core.ObjectCollection.create()

            # Create a new sketch on the xy plane.
            xyPlane = rootComp.xYConstructionPlane
            cup = sketches.add(xyPlane)
            straps = sketches.add(xyPlane)
            front = sketches.add(xyPlane)
            back = sketches.add(xyPlane)

            # Create pattern for cup.
            cupPoints.add(adsk.core.Point3D.create(1.5,12,0)) # point A (might need to adjust y)
            cupPoints.add(adsk.core.Point3D.create(0,12,0)) # (adjust y to same point as above)
            cupPoints.add(adsk.core.Point3D.create(-3,0,0)) # point B
            for i in range(cupPoints.count-1):
                pt1 = cupPoints.item(i)
                pt2 = cupPoints.item(i+1)
                cup.sketchCurves.sketchLines.addByTwoPoints(pt1, pt2)

            splinePoints.add(adsk.core.Point3D.create(-3,0,0)) # same as point B
            splinePoints.add(adsk.core.Point3D.create(2,-1,0)) # same as point B
            if cupSize > 2:
                pointC = adsk.core.Point3D.create(6 + cupSize,1,0)
                splinePoints.add(adsk.core.Point3D.create(pointC)) # point C
            else:      
                pointC = adsk.core.Point3D.create(6 + cupSize,0,0)        
                splinePoints.add(pointC) 
            cupLength = cup.sketchCurves.sketchFittedSplines.add(splinePoints)
            cupLength = (cupLength.length) # * 0.39370

            splinePoints2.add(adsk.core.Point3D.create(1.5,12,0)) # same as point A
            if cupSize > 3:
                splinePoints2.add(adsk.core.Point3D.create(4+1,4+1,0)) # adjust x and y
            else: 
                splinePoints2.add(adsk.core.Point3D.create(4,4,0))
                splinePoints2.add(pointC)
            cup.sketchCurves.sketchFittedSplines.add(splinePoints2)

            cup.name = "cups"

            # Create pattern for straps.
            lines = straps.sketchCurves.sketchLines 
            recLines = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(1.6, 10, 0))
            straps.name = "straps"

            # Create pattern for front panel.
            bodicePoints.add(adsk.core.Point3D.create(0,0,0)) # point 1
            bodicePoints.add(adsk.core.Point3D.create(0,4,0)) # point 2 (adjust y ?)
            bodicePoints.add(adsk.core.Point3D.create(cupLength*0.85,5,0)) # x adjusted according to cupLength (adjust y?)
            bodicePoints.add(adsk.core.Point3D.create(cupLength*0.85*2,4,0)) # point 2 mirrored (adjust x, same y as point 2)
            bodicePoints.add(adsk.core.Point3D.create(cupLength*0.85*2,0,0)) # point 1 mirrored 
            for i in range(bodicePoints.count-1):
                pt1 = bodicePoints.item(i)
                pt2 = bodicePoints.item(i+1)
                front.sketchCurves.sketchLines.addByTwoPoints(pt1, pt2)   
            front.name = "frontPanel"

            # Create pattern for back panel.
            lines = back.sketchCurves.sketchLines 
            recLines = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(float(upperBust*0.45), 4, 0)) # adjust y
            back.name = "backPanels"
        
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Event handler that reacts to when the command is destroyed. This terminates the script.                             
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
            
# Get dimensions of rectangle
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:

            # Get the command that was created.
            cmd = adsk.core.Command.cast(args.command)

            # Connect to the command executer event.
            onExecute = MyCommandExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)

            # Connect to the command destroyed event.
            onDestroy = MyCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            handlers.append(onDestroy)

            # Get the CommandInputs collection associated with the command.
            inputs = cmd.commandInputs

            # Create a tab input.
            tabCmdInput1 = inputs.addTabCommandInput(commandId + 'tab_1', 'Measurements')
            tab1ChildInputs = tabCmdInput1.children

            # Create an editable textbox input.
            input2 = tab1ChildInputs.addValueInput(commandId + 'w', 'Upper-Bust Circumfrence', design.unitsManager.defaultLengthUnits, adsk.core.ValueInput.createByReal(0.00))
            input1 = tab1ChildInputs.addValueInput(commandId + 'l', 'Bust Circumfrence', design.unitsManager.defaultLengthUnits, adsk.core.ValueInput.createByReal(0.00))

        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def run(context):
    try:

        # Get the existing command definition or create it if it doesn't already exist.
        cmdDef = ui.commandDefinitions.itemById(commandId)
        if not cmdDef:
            cmdDef = ui.commandDefinitions.addButtonDefinition(commandId, commandName, commandDescription)


        # Connect to the command created event.
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        # Execute the command definition.
        cmdDef.execute()

        # Prevent this module from being terminated when the script returns, because we are waiting for event handlers to fire.
        adsk.autoTerminate(False)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
#Author-Michelle
#Description-Gathered dress sewing pattern

import adsk.core, adsk.fusion, adsk.cam, traceback

app = adsk.core.Application.get()
ui  = app.userInterface
design = app.activeProduct
rootComp = design.rootComponent 
sketches = rootComp.sketches
handlers = [] # Global set of event handlers to keep them referenced for the duration of the command
commandId = 'cmdInput'
commandName = 'Gathered Dress'
commandDescription = 'Script to create a dress pattern.'

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

            Length = float(Length.value)
            Width = float(Width.value)

            # Create an object collection for the points.
            points = adsk.core.ObjectCollection.create()

            # Create a new sketch on the xy plane.
            xyPlane = rootComp.xYConstructionPlane
            chest = sketches.add(xyPlane)
            back = sketches.add(xyPlane)
            straps = sketches.add(xyPlane)
            tier1 = sketches.add(xyPlane)
            tier2 = sketches.add(xyPlane)
            # Create pattern for front chest part of the dress.
            points.add(adsk.core.Point3D.create(-(Width/4)-2,0,0)) # Point a.
            points.add(adsk.core.Point3D.create(-(Width/4)-2,(Length*0.25)*0.70,0)) # Point b.
            points.add(adsk.core.Point3D.create(-((Width/4)-2)*0.7,(Length*0.25)+2,0)) # Point c. !!!
            points.add(adsk.core.Point3D.create(0,(Length*0.25)+2,0)) # Point d.
            points.add(adsk.core.Point3D.create(((Width/4)-2)*0.3,(Length*0.25)+2,0)) # Point c mirrored. !!!
            points.add(adsk.core.Point3D.create((Width/4)+2,(Length*0.25)*0.70,0)) # Point b mirrored.
            points.add(adsk.core.Point3D.create((Width/4)+2,0,0)) # Point a mirrored.
            points.add(adsk.core.Point3D.create(0,0,0)) # Point e.   
            points.add(adsk.core.Point3D.create(-(Width/4)-2,0,0)) # Point a.

            for i in range(points.count-1):
                pt1 = points.item(i)
                pt2 = points.item(i+1)
                chest.sketchCurves.sketchLines.addByTwoPoints(pt1, pt2)   
            chest.name = "frontChest"

            # Create pattern for back chest part of the dress.
            lines = back.sketchCurves.sketchLines # Draw two connected lines.
            recLines= lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(float(Width/2), float((Length*0.25)*0.70), 0)) # Draw a rectangle by two points.
            back.name = "backChest"

            # Create pattern for straps of the dress.
            lines = straps.sketchCurves.sketchLines 
            recLines = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(3, float((Length*0.4)+2), 0))
            straps.name = "straps"

            # Create pattern for tier1 of the dress.
            lines = tier1.sketchCurves.sketchLines 
            recLines = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(float(((Width/2)*1.5)+2), float((Length*0.30)+2), 0))
            tier1.name = "tier1"

            # Create pattern for tier2 of the dress.
            lines = tier2.sketchCurves.sketchLines 
            recLines = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(float(((Width/2)*2.25)+2), float((Length*0.20)+2), 0))
            tier2.name = "tier2"
        
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
            input1 = tab1ChildInputs.addValueInput(commandId + 'l', 'Length of Dress', design.unitsManager.defaultLengthUnits, adsk.core.ValueInput.createByReal(0.00))
            input2 = tab1ChildInputs.addValueInput(commandId + 'w', 'Width of Bust', design.unitsManager.defaultLengthUnits, adsk.core.ValueInput.createByReal(0.00))

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



import adsk.core, adsk.fusion, adsk.cam, traceback

app = None
ui  = None
commandId = 'DialogTextChange'
commandName = 'Design your pouch'
commandDescription = 'Make it easy to customize your pouch'

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
            #selInput = tab1ChildInputs.itemById(commandId + '_sel')
            input1 = tab1ChildInputs.itemById(commandId + '_string')
            input2 = tab1ChildInputs.itemById(commandId + '_checkbox')
            length_input = tab1ChildInputs.itemById(commandId + '_value1')
            width_input = tab1ChildInputs.itemById(commandId + '_value2')
            
            design = app.activeProduct
            rootComp = design.rootComponent
            # Create a new sketch on the xy plane.	
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)

            length = int(length_input.value)
            width = int(width_input.value)
            offsetXY = 1
            # Draw a rectangle by two points.
            lines = sketch.sketchCurves.sketchLines

            if not input2:
                recLines1 = lines.addTwoPointRectangle(adsk.core.Point3D.create(offsetXY, offsetXY, 0), adsk.core.Point3D.create(width+offsetXY, length+offsetXY, 0))
                recLines2 = lines.addTwoPointRectangle(adsk.core.Point3D.create(offsetXY +offsetXY+ width, offsetXY, 0), adsk.core.Point3D.create( 2*(width+offsetXY), length + offsetXY, 0))
            else: 
                length = length/2
                recLines1_1 = lines.addTwoPointRectangle(adsk.core.Point3D.create(offsetXY, offsetXY, 0), adsk.core.Point3D.create(width+offsetXY, length+offsetXY, 0))
                recLines1_2 = lines.addTwoPointRectangle(adsk.core.Point3D.create(offsetXY +offsetXY+ width, offsetXY, 0), adsk.core.Point3D.create( 2*(width+offsetXY), length + offsetXY, 0))
                

            

            if input1.value:
                ui.messageBox('just testing' + input1.value + str(length_input.value) + ',' + str(width_input.value))
            

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

            #selInput = tab1ChildInputs.addSelectionInput(commandId + '_sel', 'Sketch', 'Select Sketch')
            #selInput.addSelectionFilter('Sketches')
            
            # Create string value input
            input1 = tab1ChildInputs.addStringValueInput(commandId + '_string', 'New Letter:', '')

            #create int value input:
            input_int1 = tab1ChildInputs.addValueInput(commandId + '_value1', 'Length', 'cm', adsk.core.ValueInput.createByReal(0.0))

            #create int value input:
            input_int2 = tab1ChildInputs.addValueInput(commandId + '_value2', 'Width', 'cm', adsk.core.ValueInput.createByReal(0.0))
            
            # Create bool value input with checkbox style
            input2 = tab1ChildInputs.addBoolValueInput(commandId + '_checkbox', 'Contrast bottom Pouch ', True, '', False)
            
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
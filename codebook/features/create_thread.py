# === Function: create_thread ===
# Description: Create thread feature on cylindrical face
# Parameters: body_name (str), thread_type (str), thread_size (str), thread_designation (str), thread_class (str), is_external (bool)
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (historical validation)
# Status: ✓ PASSED
# API Ref: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ThreadFeatureSample_Sample.htm

import adsk.core, adsk.fusion

def create_thread(body_name: str, thread_type: str = 'ISO Metric profile', 
                 thread_size: str = '20.0', thread_designation: str = 'M20x2.5',
                 thread_class: str = '4g6g', is_external: bool = True):
    """
    Create thread feature on a cylindrical body.
    
    Args:
        body_name: Name of the target body (must exist in root component)
        thread_type: Thread type (default 'ISO Metric profile')
        thread_size: Thread size (default '20.0' for M20)
        thread_designation: Thread designation (default 'M20x2.5')
        thread_class: Thread class (default '4g6g' for external)
        is_external: True for external thread, False for internal
    
    Returns:
        adsk.fusion.ThreadFeature: The created thread feature
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
    
    # Find the target body
    body = None
    for i in range(rootComp.bRepBodies.count):
        b = rootComp.bRepBodies.item(i)
        if b.name == body_name:
            body = b
            break
    
    if not body:
        raise ValueError(f'Body "{body_name}" not found')
    
    # Find cylindrical face
    cyl_face = None
    for j in range(body.faces.count):
        face = body.faces.item(j)
        # Check if face geometry is a cylinder (has radius attribute)
        if hasattr(face.geometry, 'radius'):
            cyl_face = face
            break
    
    if not cyl_face:
        raise ValueError(f'No cylindrical face found on body "{body_name}"')
    
    # Get thread features and data query
    threadFeatures = rootComp.features.threadFeatures
    threadDataQuery = threadFeatures.threadDataQuery
    
    # Create ThreadInfo
    threadInfo = threadFeatures.createThreadInfo(
        not is_external,  # isInternal = not is_external
        thread_type,
        thread_designation,
        thread_class
    )
    
    # Create thread feature
    faces = adsk.core.ObjectCollection.create()
    faces.add(cyl_face)
    
    threadInput = threadFeatures.createInput(faces, threadInfo)
    threadInput.isFullLength = True
    threadInput.isModeled = True  # Physical thread
    
    thread = threadFeatures.add(threadInput)
    
    print(f'Thread feature created: {thread.name}')
    return thread

# Test: Create M20x2.5 external thread on "ThreadTarget" body
# Note: First create a cylinder with diameter=20mm, then call this function
create_thread("ThreadTarget", "ISO Metric profile", "20.0", "M20x2.5", "4g6g", True)

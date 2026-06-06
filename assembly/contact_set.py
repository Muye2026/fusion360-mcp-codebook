# === Function: create_contact_set ===
# Description: Create a contact set between occurrences or bodies in an assembly
# Parameters: entities (list) - list of Occurrence or BRepBody objects
# Tested: 2026-06-06 on Fusion 360 v2703.1.11 (Mac)
# MCP Server: frankhommers/autodesk-fusion-mcp (HTTP :8765)
# Status: ✓ PASSED
# Best practice: ContactSets is on design object, not rootComp; add() takes Python list, not ObjectCollection

import adsk.core, adsk.fusion

def create_contact_set(entity_indices=None):
    """Create a contact set from occurrences by index.
    
    Args:
        entity_indices: list of occurrence indices to include in contact set.
                        If None, includes all occurrences.
    
    Returns:
        ContactSet object
    """
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent

    if entity_indices is None:
        # Include all occurrences
        entity_indices = list(range(rootComp.occurrences.count))

    # Collect occurrences
    entities = []
    for idx in entity_indices:
        occ = rootComp.occurrences.item(idx)
        if occ:
            entities.append(occ)

    if len(entities) < 2:
        return None

    # ContactSets is on design, not rootComp
    # add() takes Python list, not ObjectCollection
    contactSets = design.contactSets
    contactSet = contactSets.add(entities)

    return contactSet

# Example: Create contact set with first two occurrences
create_contact_set([0, 1])

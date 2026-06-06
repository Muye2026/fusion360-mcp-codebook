"""
Fusion 360 API Documentation Lookup Utility

This module provides a function to search Fusion 360 API documentation
by introspecting the adsk module at runtime. It replicates the functionality
of Autodesk's official get_api_documentation MCP tool.

Usage with frankhommers MCP:
    execute_python code containing:
    result = lookup_api_docs("ExtrudeFeature", "class_name")
    print(result)
"""

import inspect
import json
import re
from types import ModuleType, FunctionType


def lookup_api_docs(search_term: str, category: str = "class_name") -> str:
    """
    Search Fusion 360 API documentation.
    
    Args:
        search_term: Term to search for (class name, member name, or description)
        category: Search category - "class_name", "member_name", "description", or "all"
    
    Returns:
        JSON string with top 3 results
    """
    import adsk
    
    MAX_RESULTS = 3
    search_term_lower = search_term.lower()
    
    # Remove adsk. prefix if present
    if search_term_lower.startswith("adsk."):
        search_term_lower = search_term_lower[5:]
    
    # Parse namespace.class.member format
    parts = search_term_lower.split(".")
    if len(parts) >= 2:
        namespace_prefix = parts[0]
        remaining = ".".join(parts[1:])
        if len(parts) >= 3:
            class_name_prefix = parts[1]
            member_search = ".".join(parts[2:])
        else:
            class_name_prefix = remaining
            member_search = None
    else:
        namespace_prefix = None
        class_name_prefix = None
        member_search = search_term_lower
    
    exact_matches = []
    matches = []
    
    # Search through adsk submodules
    for namespace_name, namespace in adsk.__dict__.items():
        if namespace_name.startswith("_") or not isinstance(namespace, ModuleType):
            continue
        if namespace_prefix and namespace_prefix != namespace_name:
            continue
        
        for class_name, class_obj in namespace.__dict__.items():
            if class_name.startswith("_") or not isinstance(class_obj, type):
                continue
            
            class_name_lower = class_name.lower()
            
            # Category: class_name
            if category in ["class_name", "all"]:
                if class_name_lower == member_search:
                    exact_matches.append((namespace_name, class_obj, None))
                elif member_search in class_name_lower:
                    matches.append((namespace_name, class_obj, None))
            
            # Category: description (class level)
            if category in ["description", "all"]:
                class_doc = class_obj.__doc__.lower() if class_obj.__doc__ else ""
                if member_search in class_doc:
                    matches.append((namespace_name, class_obj, None))
            
            # Category: member_name or description (member level)
            if category in ["member_name", "description", "all"]:
                for member_name, member_obj in class_obj.__dict__.items():
                    if member_name.startswith("_"):
                        continue
                    if member_name in ["thisown", "cast"]:
                        continue
                    if not isinstance(member_obj, (property, FunctionType)):
                        continue
                    
                    member_name_lower = member_name.lower()
                    
                    # member_name category
                    if category in ["member_name", "all"]:
                        if member_name_lower == member_search:
                            exact_matches.append((namespace_name, class_obj, member_obj))
                        elif member_search in member_name_lower:
                            matches.append((namespace_name, class_obj, member_obj))
                    
                    # description category (member level)
                    if category in ["description", "all"]:
                        member_doc = member_obj.__doc__.lower() if member_obj.__doc__ else ""
                        if member_search in member_doc:
                            matches.append((namespace_name, class_obj, member_obj))
                    
                    if len(exact_matches) >= MAX_RESULTS:
                        break
                
                if len(exact_matches) >= MAX_RESULTS:
                    break
        
        if len(exact_matches) >= MAX_RESULTS:
            break
    
    # Format results
    results = []
    for namespace_name, class_obj, member_obj in (exact_matches + matches)[:MAX_RESULTS]:
        if member_obj is None:
            # Class result
            result = {
                "type": "class",
                "name": class_obj.__name__,
                "namespace": f"adsk.{namespace_name}",
                "doc": class_obj.__doc__[:500] if class_obj.__doc__ else ""
            }
            # Add key members
            properties = []
            functions = []
            for m_name, m_obj in class_obj.__dict__.items():
                if m_name.startswith("_") or m_name in ["thisown", "cast"]:
                    continue
                if isinstance(m_obj, property):
                    properties.append({"name": m_name, "doc": m_obj.__doc__[:100] if m_obj.__doc__ else ""})
                elif isinstance(m_obj, FunctionType) and len(functions) < 5:
                    try:
                        sig = str(inspect.signature(m_obj))
                        functions.append({"name": m_name, "sig": sig})
                    except:
                        functions.append({"name": m_name})
                if len(properties) >= 5 and len(functions) >= 5:
                    break
            if properties:
                result["properties"] = properties
            if functions:
                result["functions"] = functions
            results.append(result)
        elif isinstance(member_obj, property):
            # Property result
            result = {
                "type": "property",
                "name": member_name,
                "class": class_obj.__name__,
                "namespace": f"adsk.{namespace_name}",
                "doc": member_obj.__doc__[:300] if member_obj.__doc__ else ""
            }
            results.append(result)
        elif isinstance(member_obj, FunctionType):
            # Function result
            result = {
                "type": "function",
                "name": member_obj.__name__,
                "class": class_obj.__name__,
                "namespace": f"adsk.{namespace_name}",
                "doc": member_obj.__doc__[:300] if member_obj.__doc__ else ""
            }
            try:
                sig = str(inspect.signature(m_obj))
                # Clean up signature
                sig = sig.replace("(self, ", "(").replace("(self)", "()")
                result["signature"] = sig
            except:
                pass
            results.append(result)
    
    return json.dumps(results, indent=2, ensure_ascii=False)


def lookup_and_print(search_term: str, category: str = "class_name"):
    """Convenience function that looks up and prints results."""
    result = lookup_api_docs(search_term, category)
    print(result)
    return result


# Test the function
if __name__ == "__main__":
    # Test cases
    print("=== Test 1: lookup ExtrudeFeature ===")
    lookup_and_print("ExtrudeFeature", "class_name")
    
    print("\n=== Test 2: lookup HoleFeature ===")
    lookup_and_print("HoleFeature", "class_name")

import frappe
import json

@frappe.whitelist()
def get_user_preferences():
    """Get current user's preferences"""
    user = frappe.session.user
    
    # Check if preferences exist
    if frappe.db.exists("User Preferences", user):
        doc = frappe.get_doc("User Preferences", user)
        return {
            "theme": doc.theme,
            "sidebar_collapsed": doc.sidebar_collapsed,
            "custom_settings": json.loads(doc.custom_settings) if doc.custom_settings else {}
        }
    else:
        # Create default preferences
        doc = frappe.get_doc({
            "doctype": "User Preferences",
            "user": user,
            "theme": "Light",
            "sidebar_collapsed": 0
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "theme": "Light",
            "sidebar_collapsed": 0,
            "custom_settings": {}
        }

@frappe.whitelist()
def update_user_preferences(**kwargs):
    """Update current user's preferences"""
    user = frappe.session.user
    
    if frappe.db.exists("User Preferences", user):
        doc = frappe.get_doc("User Preferences", user)
    else:
        doc = frappe.get_doc({
            "doctype": "User Preferences",
            "user": user
        })
    
    # Update fields
    for key, value in kwargs.items():
        if key == "custom_settings":
            doc.custom_settings = json.dumps(value)
        elif hasattr(doc, key):
            setattr(doc, key, value)
    
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    
    return {"success": True}
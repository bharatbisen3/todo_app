# # Copyright (c) 2026, bharat and contributors
# # For license information, please see license.txt

# # import frappe
# from frappe.model.document import Document


# class UserPreferences(Document):
# 	pass








import frappe
from frappe.model.document import Document

class UserPreferences(Document):
    def validate(self):
        # Ensure user can only modify their own preferences
        if self.user != frappe.session.user and not frappe.has_permission("User Preferences", "write"):
            frappe.throw("You can only modify your own preferences")
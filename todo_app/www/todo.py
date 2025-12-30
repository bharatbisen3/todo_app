# import frappe

# def get_context(context):
#     context.no_cache = 1


import frappe

def get_context(context):
    context.no_cache = 1

    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/todo"
        raise frappe.Redirect




# import frappe
# import os

# def get_context(context):
#     context.no_cache = 1
    
#     # Read the built index.html
#     app_path = frappe.get_app_path('todo_app')
#     index_path = os.path.join(app_path, 'public', 'frontend', 'index.html')
    
#     if not os.path.exists(index_path):
#         frappe.throw("Build not found. Run 'yarn build' first")
    
#     with open(index_path, 'r', encoding='utf-8') as f:
#         html = f.read()
    
#     # Pass HTML directly to template
#     context.html_content = html
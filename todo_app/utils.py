import frappe

@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    from frappe.auth import LoginManager

    lm = LoginManager()
    lm.authenticate(usr, pwd)
    lm.post_login()

    redirect_to = frappe.form_dict.get("redirect-to") or "/todo"

    return {
        "message": "Logged In",
        "redirect_to": redirect_to
    }

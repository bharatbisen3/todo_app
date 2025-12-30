import frappe

def boot_session(bootinfo):
    """Boot session for frontend"""
    bootinfo['rzp_test_RuyXufSWvM8P3y'] = frappe.conf.get('rzp_test_RuyXufSWvM8P3y', '')
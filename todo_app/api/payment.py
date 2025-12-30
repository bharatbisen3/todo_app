import frappe
import razorpay
import hmac
import hashlib

@frappe.whitelist()
def create_payment_order(amount, email, phone, customer_name, description=None):
    """Payment order banao"""
    try:
        settings = frappe.get_single("Razorpay Settings")
        
        client = razorpay.Client(auth=(settings.api_key, settings.api_secret))
        
        # Order create karo
        order_data = {
            "amount": int(float(amount) * 100),  # paise mein
            "currency": "INR",
            "receipt": frappe.generate_hash(length=10),
        }
        
        order = client.order.create(data=order_data)
        
        # Database me save karo
        doc = frappe.get_doc({
            "doctype": "Payment Gateway Transaction",
            "customer_name": customer_name,
            "amount": amount,
            "email": email,
            "phone": phone,
            "description": description,
            "razorpay_order_id": order['id'],
            "payment_status": "Pending"
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "order_id": order['id'],
            "amount": amount,
            "currency": "INR",
            "key": settings.api_key,
            "name": doc.name
        }
    except Exception as e:
        frappe.log_error(f"Payment Order Error: {str(e)}")
        return {"success": False, "message": str(e)}

@frappe.whitelist()
def verify_payment(payment_name, razorpay_payment_id, razorpay_order_id, razorpay_signature):
    """Payment verify karo"""
    try:
        settings = frappe.get_single("Razorpay Settings")
        
        # Signature verify karo
        generated_signature = hmac.new(
            settings.api_secret.encode(),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        doc = frappe.get_doc("Payment Gateway Transaction", payment_name)
        
        if generated_signature == razorpay_signature:
            doc.razorpay_payment_id = razorpay_payment_id
            doc.razorpay_signature = razorpay_signature
            doc.payment_status = "Success"
            doc.payment_date = frappe.utils.now()
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            return {"success": True, "message": "Payment verified successfully"}
        else:
            doc.payment_status = "Failed"
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            return {"success": False, "message": "Payment verification failed"}
    except Exception as e:
        frappe.log_error(f"Payment Verification Error: {str(e)}")
        return {"success": False, "message": str(e)}
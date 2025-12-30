# # Copyright (c) 2025, bharat and contributors
# # For license information, please see license.txt

# # import frappe
# from frappe.model.document import Document


# class TodoPayment(Document):
# 	pass











# Copyright (c) 2025, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import razorpay
import hmac
import hashlib

class TodoPayment(Document):
	def validate(self):
		"""Validation before saving"""
		if self.amount <= 0:
			frappe.throw("Amount must be greater than 0")
	
	def before_insert(self):
		"""Create Razorpay order before inserting document"""
		if not self.razorpay_order_id:
			self.create_razorpay_order()
	
	def create_razorpay_order(self):
		"""Create order in Razorpay"""
		try:
			# Get Razorpay credentials from site config
			key_id = frappe.conf.get('razorpay_key_id')
			key_secret = frappe.conf.get('razorpay_key_secret')
			
			if not key_id or not key_secret:
				frappe.throw("Razorpay API keys not configured in site config")
			
			# Initialize Razorpay client
			client = razorpay.Client(auth=(key_id, key_secret))
			
			# Create order
			order_data = {
				'amount': int(self.amount * 100),  # Amount in paise
				'currency': 'INR',
				'receipt': self.name,
				'notes': {
					'todo_item': self.todo_item,
					'doctype': 'Todo Payment',
					'docname': self.name
				}
			}
			
			order = client.order.create(data=order_data)
			
			# Save order ID
			self.razorpay_order_id = order['id']
			self.payment_status = 'Pending'
			
		except Exception as e:
			frappe.log_error(f"Razorpay Order Creation Error: {str(e)}")
			frappe.throw(f"Error creating payment order: {str(e)}")


@frappe.whitelist()
def create_payment(todo_item, amount):
	"""API to create new payment"""
	try:
		# Check if todo item exists
		if not frappe.db.exists("Todo Item", todo_item):
			frappe.throw("Todo Item not found")
		
		# Create payment document
		payment = frappe.get_doc({
			'doctype': 'Todo Payment',
			'todo_item': todo_item,
			'amount': float(amount),
			'payment_status': 'Pending'
		})
		payment.insert()
		frappe.db.commit()
		
		return {
			'success': True,
			'payment_id': payment.name,
			'razorpay_order_id': payment.razorpay_order_id,
			'amount': payment.amount,
			'key_id': frappe.conf.get('razorpay_key_id')
		}
		
	except Exception as e:
		frappe.log_error(f"Payment Creation Error: {str(e)}")
		return {
			'success': False,
			'message': str(e)
		}


@frappe.whitelist()
def verify_payment(payment_id, razorpay_payment_id, razorpay_order_id, razorpay_signature):
	"""Verify payment after successful transaction"""
	try:
		# Get payment document
		payment = frappe.get_doc('Todo Payment', payment_id)
		
		# Get secret key
		key_secret = frappe.conf.get('razorpay_key_secret')
		
		# Verify signature
		generated_signature = hmac.new(
			key_secret.encode(),
			f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
			hashlib.sha256
		).hexdigest()
		
		if generated_signature == razorpay_signature:
			# Payment verified successfully
			payment.razorpay_payment_id = razorpay_payment_id
			payment.razorpay_signature = razorpay_signature
			payment.payment_status = 'Success'
			payment.payment_date = frappe.utils.now()
			payment.save()
			frappe.db.commit()
			
			return {
				'success': True,
				'message': 'Payment verified successfully'
			}
		else:
			# Signature mismatch
			payment.payment_status = 'Failed'
			payment.error_message = 'Signature verification failed'
			payment.save()
			frappe.db.commit()
			
			return {
				'success': False,
				'message': 'Payment verification failed'
			}
			
	except Exception as e:
		frappe.log_error(f"Payment Verification Error: {str(e)}")
		return {
			'success': False,
			'message': str(e)
		}


@frappe.whitelist()
def handle_payment_failure(payment_id, error_description):
	"""Handle payment failure"""
	try:
		payment = frappe.get_doc('Todo Payment', payment_id)
		payment.payment_status = 'Failed'
		payment.error_message = error_description
		payment.save()
		frappe.db.commit()
		
		return {
			'success': True,
			'message': 'Payment failure recorded'
		}
		
	except Exception as e:
		frappe.log_error(f"Payment Failure Handler Error: {str(e)}")
		return {
			'success': False,
			'message': str(e)
		}
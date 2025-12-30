<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Payments</h1>
      <p class="text-gray-500 mt-1">Manage your todo item payments</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Successful</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.success }}</p>
          </div>
          <CheckCircle class="w-10 h-10 text-green-500" />
        </div>
      </div>
      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-yellow-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Pending</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.pending }}</p>
          </div>
          <Clock class="w-10 h-10 text-yellow-500" />
        </div>
      </div>
      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Failed</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.failed }}</p>
          </div>
          <XCircle class="w-10 h-10 text-red-500" />
        </div>
      </div>
      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">Total Amount</p>
            <p class="text-2xl font-bold text-gray-900">₹{{ stats.totalAmount }}</p>
          </div>
          <IndianRupee class="w-10 h-10 text-blue-500" />
        </div>
      </div>
    </div>

    <!-- New Payment Section -->
    <div class="bg-white rounded-lg shadow mb-6">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold text-gray-900">Create New Payment</h2>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Select Todo Item
            </label>
            <select 
              v-model="newPayment.todoItem"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              :disabled="loadingTodos"
            >
              <option value="">{{ loadingTodos ? 'Loading...' : 'Select a todo item' }}</option>
              <option 
                v-for="todo in todoItems" 
                :key="todo.name" 
                :value="todo.name"
              >
                {{ todo.name }} - {{ todo.task_title }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Amount (₹)
            </label>
            <input 
              v-model.number="newPayment.amount"
              type="number"
              min="1"
              step="0.01"
              placeholder="Enter amount"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div class="flex items-end">
            <button
              @click="createPayment"
              :disabled="!newPayment.todoItem || !newPayment.amount || creatingPayment"
              class="w-full bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
            >
              <CreditCard class="w-5 h-5" />
              {{ creatingPayment ? 'Processing...' : 'Create & Pay' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter & Search -->
    <div class="bg-white rounded-lg shadow mb-6 p-4">
      <div class="flex gap-4 items-center">
        <div class="flex-1">
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Search by payment ID or todo item..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <select 
          v-model="statusFilter"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Status</option>
          <option value="Success">Success</option>
          <option value="Pending">Pending</option>
          <option value="Failed">Failed</option>
        </select>
        <button
          @click="loadPayments"
          class="px-6 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center gap-2"
        >
          <RefreshCw class="w-4 h-4" />
          Refresh
        </button>
      </div>
    </div>

    <!-- Payments List -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold text-gray-900">Payment History</h2>
      </div>
      
      <div v-if="loadingPayments" class="p-8 text-center">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">Loading payments...</p>
      </div>

      <div v-else-if="filteredPayments.length === 0" class="p-8 text-center">
        <FileText class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-600">No payments found</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Payment ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Todo Item</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr 
              v-for="payment in filteredPayments" 
              :key="payment.name"
              class="hover:bg-gray-50 transition-colors"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="font-mono text-sm text-gray-900">{{ payment.name }}</span>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">{{ payment.todo_item }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="text-sm font-semibold text-gray-900">₹{{ payment.amount }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  class="px-3 py-1 rounded-full text-xs font-semibold"
                  :class="{
                    'bg-green-100 text-green-800': payment.payment_status === 'Success',
                    'bg-yellow-100 text-yellow-800': payment.payment_status === 'Pending',
                    'bg-red-100 text-red-800': payment.payment_status === 'Failed'
                  }"
                >
                  {{ payment.payment_status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                {{ formatDate(payment.payment_date || payment.creation) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex gap-2">
                  <button
                    v-if="payment.payment_status === 'Pending'"
                    @click="retryPayment(payment)"
                    class="text-blue-600 hover:text-blue-800 font-medium text-sm flex items-center gap-1"
                  >
                    <CreditCard class="w-4 h-4" />
                    Pay Now
                  </button>
                  <button
                    @click="viewDetails(payment)"
                    class="text-gray-600 hover:text-gray-800 font-medium text-sm flex items-center gap-1"
                  >
                    <Eye class="w-4 h-4" />
                    View
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Payment Details Modal -->
    <div 
      v-if="showDetailsModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showDetailsModal = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b flex justify-between items-center">
          <h3 class="text-xl font-semibold">Payment Details</h3>
          <button @click="showDetailsModal = false" class="text-gray-400 hover:text-gray-600">
            <X class="w-6 h-6" />
          </button>
        </div>
        
        <div v-if="selectedPayment" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600">Payment ID</p>
              <p class="font-semibold">{{ selectedPayment.name }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Status</p>
              <span 
                class="inline-block px-3 py-1 rounded-full text-xs font-semibold"
                :class="{
                  'bg-green-100 text-green-800': selectedPayment.payment_status === 'Success',
                  'bg-yellow-100 text-yellow-800': selectedPayment.payment_status === 'Pending',
                  'bg-red-100 text-red-800': selectedPayment.payment_status === 'Failed'
                }"
              >
                {{ selectedPayment.payment_status }}
              </span>
            </div>
            <div>
              <p class="text-sm text-gray-600">Todo Item</p>
              <p class="font-semibold">{{ selectedPayment.todo_item }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Amount</p>
              <p class="font-semibold text-lg">₹{{ selectedPayment.amount }}</p>
            </div>
            <div v-if="selectedPayment.razorpay_order_id">
              <p class="text-sm text-gray-600">Razorpay Order ID</p>
              <p class="font-mono text-xs">{{ selectedPayment.razorpay_order_id }}</p>
            </div>
            <div v-if="selectedPayment.razorpay_payment_id">
              <p class="text-sm text-gray-600">Razorpay Payment ID</p>
              <p class="font-mono text-xs">{{ selectedPayment.razorpay_payment_id }}</p>
            </div>
            <div v-if="selectedPayment.payment_method">
              <p class="text-sm text-gray-600">Payment Method</p>
              <p class="font-semibold">{{ selectedPayment.payment_method }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Created On</p>
              <p class="font-semibold">{{ formatDate(selectedPayment.creation) }}</p>
            </div>
            <div v-if="selectedPayment.payment_date" class="col-span-2">
              <p class="text-sm text-gray-600">Payment Date</p>
              <p class="font-semibold">{{ formatDate(selectedPayment.payment_date) }}</p>
            </div>
            <div v-if="selectedPayment.error_message" class="col-span-2">
              <p class="text-sm text-gray-600">Error Message</p>
              <p class="text-red-600 text-sm">{{ selectedPayment.error_message }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { call } from 'frappe-ui'
import { 
  CreditCard, CheckCircle, Clock, XCircle, IndianRupee, 
  RefreshCw, Eye, X, FileText 
} from 'lucide-vue-next'

const todoItems = ref([])
const payments = ref([])
const loadingTodos = ref(false)
const loadingPayments = ref(false)
const creatingPayment = ref(false)
const searchQuery = ref('')
const statusFilter = ref('all')
const showDetailsModal = ref(false)
const selectedPayment = ref(null)

const newPayment = ref({
  todoItem: '',
  amount: null
})

const stats = computed(() => {
  return {
    success: payments.value.filter(p => p.payment_status === 'Success').length,
    pending: payments.value.filter(p => p.payment_status === 'Pending').length,
    failed: payments.value.filter(p => p.payment_status === 'Failed').length,
    totalAmount: payments.value
      .filter(p => p.payment_status === 'Success')
      .reduce((sum, p) => sum + (p.amount || 0), 0)
      .toFixed(2)
  }
})

const filteredPayments = computed(() => {
  let filtered = payments.value

  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(p => p.payment_status === statusFilter.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(p => 
      p.name.toLowerCase().includes(query) ||
      p.todo_item.toLowerCase().includes(query)
    )
  }

  return filtered
})

onMounted(() => {
  loadTodoItems()
  loadPayments()
  loadRazorpayScript()
})

async function loadTodoItems() {
  loadingTodos.value = true
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Todo Item',
      fields: ['name', 'task_title', 'status'],
      limit_page_length: 100
    })
    todoItems.value = response || []
  } catch (error) {
    console.error('Error loading todos:', error)
    showNotification('Failed to load todo items', 'error')
  } finally {
    loadingTodos.value = false
  }
}

async function loadPayments() {
  loadingPayments.value = true
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Todo Payment',
      fields: [
        'name', 'todo_item', 'amount', 'payment_status',
        'razorpay_order_id', 'razorpay_payment_id', 
        'payment_date', 'payment_method', 'error_message',
        'creation'
      ],
      order_by: 'creation desc',
      limit_page_length: 100
    })
    payments.value = response || []
  } catch (error) {
    console.error('Error loading payments:', error)
    showNotification('Failed to load payments', 'error')
  } finally {
    loadingPayments.value = false
  }
}

async function createPayment() {
  if (!newPayment.value.todoItem || !newPayment.value.amount) {
    showNotification('Please fill all fields', 'error')
    return
  }

  creatingPayment.value = true
  try {
    const response = await call(
      'todo_app.todo_app.doctype.todo_payment.todo_payment.create_payment',
      {
        todo_item: newPayment.value.todoItem,
        amount: newPayment.value.amount
      }
    )

    if (response && response.success) {
      showNotification('Payment created successfully', 'success')
      newPayment.value = { todoItem: '', amount: null }
      await loadPayments()
      
      setTimeout(() => {
        openRazorpayCheckout(response)
      }, 500)
    } else {
      showNotification(response.message || 'Failed to create payment', 'error')
    }
  } catch (error) {
    console.error('Error creating payment:', error)
    showNotification('Failed to create payment', 'error')
  } finally {
    creatingPayment.value = false
  }
}

function loadRazorpayScript() {
  if (document.getElementById('razorpay-script')) return

  const script = document.createElement('script')
  script.id = 'razorpay-script'
  script.src = 'https://checkout.razorpay.com/v1/checkout.js'
  document.head.appendChild(script)
}

function openRazorpayCheckout(paymentData) {
  if (typeof Razorpay === 'undefined') {
    showNotification('Razorpay not loaded. Please refresh the page.', 'error')
    return
  }

  const options = {
    key: paymentData.key_id,
    amount: paymentData.amount * 100,
    currency: 'INR',
    name: 'Todo App',
    description: 'Payment for Todo Item',
    order_id: paymentData.razorpay_order_id,
    handler: async function(response) {
      await verifyPayment(
        paymentData.payment_id,
        response.razorpay_payment_id,
        response.razorpay_order_id,
        response.razorpay_signature
      )
    },
    theme: {
      color: '#3B82F6'
    },
    modal: {
      ondismiss: function() {
        showNotification('Payment cancelled', 'info')
      }
    }
  }

  const rzp = new Razorpay(options)

  rzp.on('payment.failed', async function(response) {
    await handlePaymentFailure(
      paymentData.payment_id,
      response.error.description
    )
  })

  rzp.open()
}

async function verifyPayment(paymentId, razorpayPaymentId, razorpayOrderId, razorpaySignature) {
  try {
    const response = await call(
      'todo_app.todo_app.doctype.todo_payment.todo_payment.verify_payment',
      {
        payment_id: paymentId,
        razorpay_payment_id: razorpayPaymentId,
        razorpay_order_id: razorpayOrderId,
        razorpay_signature: razorpaySignature
      }
    )

    if (response && response.success) {
      showNotification('Payment successful!', 'success')
      await loadPayments()
    } else {
      showNotification('Payment verification failed', 'error')
    }
  } catch (error) {
    console.error('Error verifying payment:', error)
    showNotification('Payment verification failed', 'error')
  }
}

async function handlePaymentFailure(paymentId, errorDescription) {
  try {
    await call(
      'todo_app.todo_app.doctype.todo_payment.todo_payment.handle_payment_failure',
      {
        payment_id: paymentId,
        error_description: errorDescription
      }
    )
    showNotification('Payment failed: ' + errorDescription, 'error')
    await loadPayments()
  } catch (error) {
    console.error('Error handling payment failure:', error)
  }
}

async function retryPayment(payment) {
  try {
    const doc = await call('frappe.client.get', {
      doctype: 'Todo Payment',
      name: payment.name
    })

    const paymentData = {
      key_id: doc.key_id,
      amount: doc.amount,
      razorpay_order_id: doc.razorpay_order_id,
      payment_id: doc.name
    }

    openRazorpayCheckout(paymentData)
  } catch (error) {
    console.error('Error retrying payment:', error)
    showNotification('Failed to retry payment', 'error')
  }
}

function viewDetails(payment) {
  selectedPayment.value = payment
  showDetailsModal.value = true
}

function formatDate(dateStr) {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function showNotification(message, type = 'info') {
  console.log(`[${type}] ${message}`)
  // You can integrate a toast library here
  alert(message)
}
</script>
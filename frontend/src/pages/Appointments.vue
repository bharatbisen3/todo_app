<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Appointments</h1>
        <p class="text-gray-600 mt-1">Manage your appointments and schedule</p>
      </div>
      <Button @click="openAddModal" variant="solid">
        + New Appointment
      </Button>
    </div>

    <!-- View Toggle -->
    <div class="mb-6 flex gap-2">
      <Button 
        @click="viewMode = 'list'" 
        :variant="viewMode === 'list' ? 'solid' : 'outline'"
        size="sm"
      >
        List View
      </Button>
      <Button 
        @click="viewMode = 'calendar'" 
        :variant="viewMode === 'calendar' ? 'solid' : 'outline'"
        size="sm"
      >
        Calendar View
      </Button>
    </div>

    <!-- Filter Tabs (Only in List View) -->
    <div v-if="viewMode === 'list'" class="flex gap-2 mb-6 flex-wrap">
      <Button
        v-for="filter in filters"
        :key="filter.value"
        @click="currentFilter = filter.value"
        :variant="currentFilter === filter.value ? 'solid' : 'outline'"
        size="sm"
      >
        {{ filter.label }} ({{ getFilterCount(filter.value) }})
      </Button>
    </div>

    <!-- List View -->
    <div v-if="viewMode === 'list'">
      <!-- Loading -->
      <div v-if="appointments.loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-2 text-gray-600">Loading appointments...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="!filteredAppointments.length" class="text-center py-12 bg-white rounded-lg shadow-sm">
        <Calendar class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-lg font-medium text-gray-900">No appointments yet</h3>
        <p class="mt-1 text-gray-500">Get started by creating your first appointment</p>
        <Button @click="openAddModal" variant="solid" class="mt-4">
          + Add Appointment
        </Button>
      </div>

      <!-- Appointments List -->
      <div v-else class="space-y-4">
        <div
          v-for="apt in filteredAppointments"
          :key="apt.name"
          class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between">
            <div class="flex gap-4 flex-1">
              <!-- Date Box -->
              <div class="w-16 h-16 rounded-lg bg-blue-50 flex flex-col items-center justify-center">
                <span class="text-xs text-blue-600 font-medium">{{ formatDay(apt.scheduled_time) }}</span>
                <span class="text-2xl font-bold text-blue-600">{{ formatDayNum(apt.scheduled_time) }}</span>
              </div>

              <!-- Details -->
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900">
                  {{ apt.customer_name }}
                </h3>
                <p class="text-sm text-gray-600 mt-1">
                  📅 {{ formatFullDate(apt.scheduled_time) }}
                </p>
                <div class="mt-2 space-y-1">
                  <p v-if="apt.customer_email" class="text-sm text-gray-600">
                    ✉️ {{ apt.customer_email }}
                  </p>
                  <p v-if="apt.customer_phone_number" class="text-sm text-gray-600">
                    📞 {{ apt.customer_phone_number }}
                  </p>
                  <p v-if="apt.customer_details" class="text-sm text-gray-500 mt-2">
                    {{ apt.customer_details }}
                  </p>
                </div>
              </div>

              <!-- Status Badge -->
              <Badge :theme="getStatusColor(apt.status)">
                {{ apt.status }}
              </Badge>
            </div>

            <!-- Actions -->
            <div class="flex gap-2 ml-4">
              <Button size="sm" variant="outline" @click="openEditModal(apt)">
                Edit
              </Button>
              <Button size="sm" variant="outline" theme="red" @click="deleteAppointment(apt)">
                Delete
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Calendar View -->
    <div v-else class="bg-white rounded-lg shadow-sm p-6">
      <FullCalendar :options="calendarOptions" />
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">
          {{ isEditing ? 'Edit Appointment' : 'New Appointment' }}
        </h2>

        <div class="space-y-4">
          <!-- Customer Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Customer Name <span class="text-red-500">*</span>
            </label>
            <Input
              v-model="formData.customer_name"
              placeholder="Enter customer name"
            />
          </div>

          <!-- Email & Phone -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Email <span class="text-red-500">*</span>
              </label>
              <Input
                v-model="formData.customer_email"
                type="email"
                placeholder="email@example.com"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Phone Number
              </label>
              <Input
                v-model="formData.customer_phone_number"
                placeholder="+91 12345 67890"
              />
            </div>
          </div>

          <!-- Scheduled Time & Status -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Scheduled Time <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formData.scheduled_time"
                type="datetime-local"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Status <span class="text-red-500">*</span>
              </label>
              <select
                v-model="formData.status"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="Open">Open</option>
                <option value="Unverified">Unverified</option>
                <option value="Closed">Closed</option>
              </select>
            </div>
          </div>

          <!-- Skype ID -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Skype ID
            </label>
            <Input
              v-model="formData.customer_skype"
              placeholder="skype_username"
            />
          </div>

          <!-- Details -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Additional Details
            </label>
            <textarea
              v-model="formData.customer_details"
              rows="4"
              placeholder="Any additional information..."
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>
        </div>

        <!-- Modal Actions -->
        <div class="mt-6 flex gap-3 justify-end">
          <Button @click="closeModal" variant="outline">
            Cancel
          </Button>
          <Button @click="saveAppointment" variant="solid" :loading="saving">
            {{ isEditing ? 'Update' : 'Create' }} Appointment
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createListResource, Button, Badge, Input } from 'frappe-ui'
import { Calendar } from 'lucide-vue-next'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

const viewMode = ref('list')
const showModal = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const currentFilter = ref('all')

const filters = [
  { label: 'All', value: 'all' },
  { label: 'Open', value: 'Open' },
  { label: 'Unverified', value: 'Unverified' },
  { label: 'Closed', value: 'Closed' }
]

const formData = ref({
  customer_name: '',
  customer_email: '',
  customer_phone_number: '',
  customer_skype: '',
  customer_details: '',
  scheduled_time: '',
  status: 'Open'
})

// Fetch appointments
const appointments = createListResource({
  doctype: 'Appointment',
  fields: [
    'name',
    'customer_name',
    'customer_email',
    'customer_phone_number',
    'customer_skype',
    'customer_details',
    'scheduled_time',
    'status'
  ],
  orderBy: 'scheduled_time desc',
  auto: true
})

// Calendar options
const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },
  events: calendarEvents.value,
  eventClick: handleEventClick,
  dateClick: handleDateClick,
  editable: true,
  selectable: true,
  selectMirror: true,
  dayMaxEvents: true,
  height: 'auto',
  eventDisplay: 'block',
}))

// Convert appointments to calendar events
const calendarEvents = computed(() => {
  if (!appointments.data) return []
  
  return appointments.data.map(apt => ({
    id: apt.name,
    title: apt.customer_name,
    start: apt.scheduled_time,
    backgroundColor: getEventColor(apt.status),
    borderColor: getEventColor(apt.status),
    extendedProps: {
      customer_email: apt.customer_email,
      customer_phone_number: apt.customer_phone_number,
      customer_details: apt.customer_details,
      status: apt.status
    }
  }))
})

// Get event color based on status
function getEventColor(status) {
  const colors = {
    'Open': '#3B82F6',      // Blue
    'Unverified': '#F59E0B', // Orange
    'Closed': '#10B981'      // Green
  }
  return colors[status] || '#6B7280'
}

// Handle event click in calendar
function handleEventClick(info) {
  const apt = appointments.data.find(a => a.name === info.event.id)
  if (apt) {
    openEditModal(apt)
  }
}

// Handle date click in calendar (to add new appointment)
function handleDateClick(info) {
  openAddModal()
  // Pre-fill the date
  const clickedDate = new Date(info.dateStr)
  formData.value.scheduled_time = formatDatetimeLocal(clickedDate)
}

// Filtered appointments
const filteredAppointments = computed(() => {
  if (!appointments.data) return []
  if (currentFilter.value === 'all') return appointments.data
  return appointments.data.filter(apt => apt.status === currentFilter.value)
})

// Get count for each filter
function getFilterCount(filter) {
  if (!appointments.data) return 0
  if (filter === 'all') return appointments.data.length
  return appointments.data.filter(apt => apt.status === filter).length
}

// Open add modal
function openAddModal() {
  isEditing.value = false
  formData.value = {
    customer_name: '',
    customer_email: '',
    customer_phone_number: '',
    customer_skype: '',
    customer_details: '',
    scheduled_time: '',
    status: 'Open'
  }
  showModal.value = true
}

// Open edit modal
function openEditModal(apt) {
  isEditing.value = true
  formData.value = {
    name: apt.name,
    customer_name: apt.customer_name,
    customer_email: apt.customer_email,
    customer_phone_number: apt.customer_phone_number || '',
    customer_skype: apt.customer_skype || '',
    customer_details: apt.customer_details || '',
    scheduled_time: formatDatetimeLocal(apt.scheduled_time),
    status: apt.status
  }
  showModal.value = true
}

// Close modal
function closeModal() {
  showModal.value = false
  formData.value = {
    customer_name: '',
    customer_email: '',
    customer_phone_number: '',
    customer_skype: '',
    customer_details: '',
    scheduled_time: '',
    status: 'Open'
  }
}

// Save appointment
async function saveAppointment() {
  // Validation
  if (!formData.value.customer_name.trim()) {
    alert('Please enter customer name')
    return
  }
  if (!formData.value.customer_email.trim()) {
    alert('Please enter customer email')
    return
  }
  if (!formData.value.scheduled_time) {
    alert('Please select scheduled time')
    return
  }

  saving.value = true

  try {
    if (isEditing.value) {
      // Update existing appointment
      await appointments.setValue.submit({
        name: formData.value.name,
        customer_name: formData.value.customer_name,
        customer_email: formData.value.customer_email,
        customer_phone_number: formData.value.customer_phone_number,
        customer_skype: formData.value.customer_skype,
        customer_details: formData.value.customer_details,
        scheduled_time: formData.value.scheduled_time,
        status: formData.value.status
      })
    } else {
      // Create new appointment
      await appointments.insert.submit({
        customer_name: formData.value.customer_name,
        customer_email: formData.value.customer_email,
        customer_phone_number: formData.value.customer_phone_number,
        customer_skype: formData.value.customer_skype,
        customer_details: formData.value.customer_details,
        scheduled_time: formData.value.scheduled_time,
        status: formData.value.status
      })
    }

    await appointments.reload()
    closeModal()
  } catch (error) {
    console.error('Error saving appointment:', error)
    alert('Failed to save appointment. Please try again.')
  } finally {
    saving.value = false
  }
}

// Delete appointment
async function deleteAppointment(apt) {
  if (!confirm(`Are you sure you want to delete appointment for ${apt.customer_name}?`)) return

  try {
    await appointments.delete.submit(apt.name)
    await appointments.reload()
  } catch (error) {
    console.error('Error deleting appointment:', error)
    alert('Failed to delete appointment')
  }
}

// Helper functions
function getStatusColor(status) {
  const colors = {
    'Open': 'blue',
    'Unverified': 'orange',
    'Closed': 'green'
  }
  return colors[status] || 'gray'
}

function formatDay(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase()
}

function formatDayNum(dateString) {
  const date = new Date(dateString)
  return date.getDate()
}

function formatFullDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', { 
    month: 'long', 
    day: 'numeric', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatDatetimeLocal(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
}
</script>

<style>
/* FullCalendar Custom Styles */
.fc {
  font-family: inherit;
}

.fc .fc-button {
  background-color: #3B82F6;
  border-color: #3B82F6;
  text-transform: capitalize;
  padding: 0.5rem 1rem;
}

.fc .fc-button:hover {
  background-color: #2563EB;
  border-color: #2563EB;
}

.fc .fc-button-active {
  background-color: #1D4ED8 !important;
  border-color: #1D4ED8 !important;
}

.fc .fc-toolbar-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
}

.fc-theme-standard td, 
.fc-theme-standard th {
  border-color: #E5E7EB;
}

.fc-daygrid-event {
  cursor: pointer;
  padding: 2px 4px;
  border-radius: 4px;
}

.fc-event-title {
  font-weight: 500;
}
</style>
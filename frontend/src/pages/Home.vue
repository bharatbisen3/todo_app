<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto py-8 px-4">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">My Tasks</h1>
        <p class="text-gray-600">Manage your daily tasks efficiently</p>
      </div>

      <!-- Add Task Form -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex gap-3 mb-4">
          <Input
            v-model="newTask.title"
            placeholder="What needs to be done?"
            class="flex-1"
            @keyup.enter="addTask"
          />
          <Button @click="addTask" variant="solid" :loading="addingTask">
            Add Task
          </Button>
        </div>
        
        <!-- Additional Fields (Collapsible) -->
        <div v-if="showAdvanced" class="space-y-3 pt-3 border-t">
          <textarea
            v-model="newTask.description"
            placeholder="Add description (optional)"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          ></textarea>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Priority</label>
              <select 
                v-model="newTask.priority" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
              <input 
                v-model="newTask.due_date" 
                type="date" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
        
        <button 
          @click="showAdvanced = !showAdvanced"
          class="mt-3 text-sm text-blue-600 hover:text-blue-700 font-medium"
        >
          {{ showAdvanced ? '− Less options' : '+ More options' }}
        </button>
      </div>

      <!-- Filter Tabs -->
      <div class="flex gap-2 mb-6 flex-wrap">
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

      <!-- Loading State -->
      <div v-if="todos.loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-2 text-gray-600">Loading tasks...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="!filteredTodos.length" class="text-center py-12 bg-white rounded-lg shadow-sm">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-2 text-lg font-medium text-gray-900">No tasks yet</h3>
        <p class="mt-1 text-gray-500">Get started by creating your first task</p>
      </div>

      <!-- Task List -->
      <div v-else class="space-y-3">
        <div
          v-for="todo in filteredTodos"
          :key="todo.name"
          class="bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start gap-4">
            <!-- Checkbox -->
            <input
              type="checkbox"
              :checked="todo.status === 'Completed'"
              @change="toggleComplete(todo)"
              class="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
            />

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2 flex-wrap">
                <h3
                  :class="[
                    'text-lg font-medium',
                    todo.status === 'Completed' ? 'line-through text-gray-500' : 'text-gray-900'
                  ]"
                >
                  {{ todo.task_title }}
                </h3>
                <div class="flex items-center gap-2">
                  <Badge
                    :theme="getPriorityColor(todo.priority)"
                    v-if="todo.priority"
                  >
                    {{ todo.priority }}
                  </Badge>
                  <Badge
                    :theme="getStatusColor(todo.status)"
                  >
                    {{ todo.status }}
                  </Badge>
                </div>
              </div>

              <p
                v-if="todo.description"
                class="mt-2 text-sm text-gray-600 whitespace-pre-wrap"
              >
                {{ todo.description }}
              </p>

              <div class="mt-2 flex items-center gap-4 text-sm text-gray-500">
                <span v-if="todo.due_date" class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {{ formatDate(todo.due_date) }}
                </span>
                <span class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ formatRelativeTime(todo.creation) }}
                </span>
              </div>

              <!-- Actions -->
              <div class="mt-3 flex gap-2">
                <Button
                  v-if="todo.status === 'Open'"
                  @click="updateStatus(todo, 'In Progress')"
                  size="sm"
                  variant="outline"
                >
                  Start
                </Button>
                <Button
                  v-if="todo.status === 'In Progress'"
                  @click="updateStatus(todo, 'Completed')"
                  size="sm"
                  variant="outline"
                  theme="green"
                >
                  Complete
                </Button>
                <Button
                  @click="deleteTask(todo)"
                  size="sm"
                  variant="outline"
                  theme="red"
                >
                  Delete
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createListResource, Button, Input, Badge } from 'frappe-ui'

const newTask = ref({
  title: '',
  description: '',
  status: 'Open',
  priority: 'Medium',
  due_date: ''
})

const showAdvanced = ref(false)
const addingTask = ref(false)
const currentFilter = ref('all')

const filters = [
  { label: 'All', value: 'all' },
  { label: 'Open', value: 'Open' },
  { label: 'In Progress', value: 'In Progress' },
  { label: 'Completed', value: 'Completed' }
]

// IMPORTANT: Using task_title because that's the field name in DocType
const todos = createListResource({
  doctype: 'Todo Item',
  fields: ['name', 'task_title', 'description', 'status', 'priority', 'due_date', 'creation'],
  orderBy: 'creation desc',
  auto: true
})

// Filtered todos based on current filter
const filteredTodos = computed(() => {
  if (!todos.data) return []
  if (currentFilter.value === 'all') return todos.data
  return todos.data.filter(todo => todo.status === currentFilter.value)
})

// Get count for each filter
function getFilterCount(filter) {
  if (!todos.data) return 0
  if (filter === 'all') return todos.data.length
  return todos.data.filter(todo => todo.status === filter).length
}

// Add new task
async function addTask() {
  if (!newTask.value.title.trim()) {
    alert('Please enter a task title')
    return
  }

  addingTask.value = true
  
  try {
    // IMPORTANT: Using task_title to match DocType field name
    await todos.insert.submit(
      {
        task_title: newTask.value.title,
        description: newTask.value.description || '',
        status: 'Open',
        priority: newTask.value.priority,
        due_date: newTask.value.due_date || null
      }
    )
    
    // Reset form
    newTask.value = {
      title: '',
      description: '',
      status: 'Open',
      priority: 'Medium',
      due_date: ''
    }
    showAdvanced.value = false
    
    // Reload list
    await todos.reload()
  } catch (error) {
    console.error('Error adding task:', error)
    alert('Failed to add task. Please try again.')
  } finally {
    addingTask.value = false
  }
}

// Toggle task completion
async function toggleComplete(todo) {
  const newStatus = todo.status === 'Completed' ? 'Open' : 'Completed'
  await updateStatus(todo, newStatus)
}

// Update task status
async function updateStatus(todo, newStatus) {
  try {
    await todos.setValue.submit({
      name: todo.name,
      status: newStatus
    })
    await todos.reload()
  } catch (error) {
    console.error('Error updating status:', error)
    alert('Failed to update task status')
  }
}

// Delete task
async function deleteTask(todo) {
  if (!confirm('Are you sure you want to delete this task?')) return

  try {
    await todos.delete.submit(todo.name)
    await todos.reload()
  } catch (error) {
    console.error('Error deleting task:', error)
    alert('Failed to delete task')
  }
}

// Helper functions
function getPriorityColor(priority) {
  const colors = {
    High: 'red',
    Medium: 'orange',
    Low: 'blue'
  }
  return colors[priority] || 'gray'
}

function getStatusColor(status) {
  const colors = {
    Open: 'blue',
    'In Progress': 'orange',
    Completed: 'green'
  }
  return colors[status] || 'gray'
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function formatRelativeTime(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now - date) / 1000)

  if (diffInSeconds < 60) return 'just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`
  return formatDate(dateString)
}
</script>

<style scoped>
/* Custom scrollbar for better UX */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
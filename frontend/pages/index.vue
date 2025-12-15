<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">Todo List</h1>
        <p class="text-gray-600">Manage your tasks efficiently</p>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
        {{ error }}
      </div>

      <!-- Success Message -->
      <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg mb-6">
        {{ success }}
      </div>

      <!-- Two Column Layout -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column: Todo List (2/3 width) -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Filters -->
          <div class="bg-white rounded-lg shadow-lg p-4">
            <div class="flex gap-2">
              <button
                @click="filter = 'all'"
                :class="['px-4 py-2 rounded-lg transition', filter === 'all' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300']"
              >
                All
              </button>
              <button
                @click="filter = 'active'"
                :class="['px-4 py-2 rounded-lg transition', filter === 'active' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300']"
              >
                Active
              </button>
              <button
                @click="filter = 'completed'"
                :class="['px-4 py-2 rounded-lg transition', filter === 'completed' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300']"
              >
                Completed
              </button>
            </div>
          </div>

          <!-- Todos List -->
          <div class="space-y-4">
            <div v-if="fetchLoading" class="text-center py-8">
              <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
              <p class="mt-2 text-gray-600">Loading todos...</p>
            </div>

            <div v-else-if="filteredTodos.length === 0" class="bg-white rounded-lg shadow-lg p-8 text-center">
              <p class="text-gray-500">No todos found. Create your first todo!</p>
            </div>

            <div
              v-for="todo in filteredTodos"
              :key="todo.id"
              class="bg-white rounded-lg shadow-lg p-6 transition hover:shadow-xl"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-3 mb-2">
                    <input
                      type="checkbox"
                      :checked="todo.completed"
                      @change="toggleTodo(todo)"
                      class="w-5 h-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-500"
                    />
                    <h3 :class="['text-lg font-semibold', todo.completed ? 'line-through text-gray-400' : 'text-gray-800']">
                      {{ todo.title }}
                    </h3>
                  </div>
                  <p :class="['ml-8', todo.completed ? 'text-gray-400' : 'text-gray-600']">
                    {{ todo.description }}
                  </p>
                </div>
                <button
                  @click="deleteTodo(todo.id)"
                  class="ml-4 text-red-600 hover:text-red-800 transition"
                  title="Delete todo"
                >
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Stats -->
          <div class="bg-white rounded-lg shadow-lg p-4">
            <div class="flex justify-between text-sm text-gray-600">
              <span>Total: {{ todos.length }}</span>
              <span>Active: {{ activeTodos }}</span>
              <span>Completed: {{ completedTodos }}</span>
            </div>
          </div>
        </div>

        <!-- Right Column: Add Todo Form (1/3 width) -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-lg p-6 sticky top-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Add New Todo</h2>
            <form @submit.prevent="addTodo" class="space-y-4">
              <div>
                <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Title</label>
                <input
                  v-model="newTodo.title"
                  id="title"
                  type="text"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Enter todo title"
                />
              </div>
              <div>
                <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  v-model="newTodo.description"
                  id="description"
                  rows="4"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Enter todo description"
                ></textarea>
              </div>
              <button
                type="submit"
                :disabled="loading"
                class="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ loading ? 'Adding...' : 'Add Todo' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// State
const todos = ref([])
const newTodo = ref({
  title: '',
  description: '',
  completed: false
})
const loading = ref(false)
const fetchLoading = ref(false)
const error = ref('')
const success = ref('')
const filter = ref('all')

// Computed
const filteredTodos = computed(() => {
  if (filter.value === 'active') {
    return todos.value.filter(todo => !todo.completed)
  } else if (filter.value === 'completed') {
    return todos.value.filter(todo => todo.completed)
  }
  return todos.value
})

const activeTodos = computed(() => todos.value.filter(todo => !todo.completed).length)
const completedTodos = computed(() => todos.value.filter(todo => todo.completed).length)

// Methods
const fetchTodos = async () => {
  try {
    fetchLoading.value = true
    error.value = ''
    const response = await fetch(`${apiBase}/todos`)
    if (!response.ok) throw new Error('Failed to fetch todos')
    todos.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    fetchLoading.value = false
  }
}

const addTodo = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = ''

    const response = await fetch(`${apiBase}/todos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newTodo.value)
    })

    if (!response.ok) throw new Error('Failed to add todo')

    const createdTodo = await response.json()
    todos.value.push(createdTodo)

    // Reset form
    newTodo.value = {
      title: '',
      description: '',
      completed: false
    }

    success.value = 'Todo added successfully!'
    setTimeout(() => success.value = '', 3000)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const toggleTodo = async (todo) => {
  try {
    error.value = ''
    const updatedTodo = { ...todo, completed: !todo.completed }

    const response = await fetch(`${apiBase}/todos/${todo.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updatedTodo)
    })

    if (!response.ok) throw new Error('Failed to update todo')

    const index = todos.value.findIndex(t => t.id === todo.id)
    if (index !== -1) {
      todos.value[index] = await response.json()
    }
  } catch (err) {
    error.value = err.message
  }
}

const deleteTodo = async (id) => {
  if (!confirm('Are you sure you want to delete this todo?')) return

  try {
    error.value = ''
    const response = await fetch(`${apiBase}/todos/${id}`, {
      method: 'DELETE'
    })

    if (!response.ok) throw new Error('Failed to delete todo')

    todos.value = todos.value.filter(todo => todo.id !== id)
    success.value = 'Todo deleted successfully!'
    setTimeout(() => success.value = '', 3000)
  } catch (err) {
    error.value = err.message
  }
}

// Fetch todos on mount
onMounted(() => {
  fetchTodos()
})
</script>

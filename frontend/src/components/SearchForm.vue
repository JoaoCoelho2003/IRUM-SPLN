<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div class="relative">
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>
      <input
        id="search-query"
        v-model="searchQuery"
        type="text"
        placeholder="Search for documents, topics, or keywords..."
        class="w-full pl-10 pr-20 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-500 focus:border-gray-500 text-gray-100 placeholder-gray-400"
        required
        :disabled="isSearching"
      />
      <div class="absolute inset-y-0 right-0 flex items-center">
        <div class="border-l border-gray-700 h-full flex items-center pr-3">
          <select
            id="top-k"
            v-model="topK"
            class="bg-gray-800 border-0 text-gray-300 text-sm rounded-md focus:outline-none focus:ring-0 cursor-pointer px-2 py-1"
            :disabled="isSearching"
            style="color-scheme: dark"
          >
            <option value="5" class="bg-gray-800 text-gray-300">5 results</option>
            <option value="10" class="bg-gray-800 text-gray-300">10 results</option>
            <option value="20" class="bg-gray-800 text-gray-300">20 results</option>
            <option value="50" class="bg-gray-800 text-gray-300">50 results</option>
          </select>
        </div>
      </div>
    </div>

    <div class="flex justify-end">
      <button
        type="submit"
        class="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-gray-100 rounded-lg transition-colors flex items-center"
        :disabled="isSearching"
      >
        <span v-if="isSearching" class="flex items-center">
          <svg
            class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-100"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          Searching...
        </span>
        <span v-else class="flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 mr-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
          Search
        </span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  initialQuery: {
    type: String,
    default: '',
  },
  isSearching: {
    type: Boolean,
    default: false,
  },
  initialTopK: {
    type: Number,
    default: 10,
  },
})

const emit = defineEmits(['search'])

const searchQuery = ref('')
const topK = ref(props.initialTopK.toString())

const handleSubmit = () => {
  if (searchQuery.value.trim()) {
    emit('search', {
      query: searchQuery.value.trim(),
      topK: parseInt(topK.value),
    })
  }
}

onMounted(() => {
  if (props.initialQuery) {
    searchQuery.value = props.initialQuery
  }
})
</script>

<style scoped>
select#top-k {
  background-color: rgb(31 41 55);
  color: rgb(209 213 219);
}

select#top-k option {
  background-color: rgb(31 41 55);
  color: rgb(209 213 219);
}

select#top-k::-webkit-scrollbar {
  width: 8px;
}

select#top-k::-webkit-scrollbar-track {
  background: rgb(55 65 81);
}

select#top-k::-webkit-scrollbar-thumb {
  background: rgb(75 85 99);
  border-radius: 4px;
}
</style>

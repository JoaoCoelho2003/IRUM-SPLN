<template>
  <div class="max-w-6xl mx-auto px-4 py-8 space-y-8 animate-fade-in">
    <div class="bg-gray-800 rounded-lg border border-gray-700 p-6">
      <div class="mb-4">
        <h1 class="text-2xl font-bold text-gray-100">Search Documents</h1>
      </div>
      <div>
        <search-form
          :initial-query="query"
          :is-searching="loading"
          :initial-top-k="topK"
          @search="handleSearch"
          @update-top-k="updateTopK"
        />
      </div>
    </div>

    <div v-if="loading" class="flex flex-col items-center justify-center py-12">
      <div
        class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-gray-400 mb-4"
      ></div>
      <p class="text-gray-400">Searching documents...</p>
    </div>

    <div
      v-else-if="error"
      class="bg-red-900/20 border border-red-800/50 text-red-200 px-4 py-3 rounded-lg"
    >
      <div class="flex items-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 mr-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <p>{{ error }}</p>
      </div>
    </div>

    <div v-else-if="results.length > 0" class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold text-gray-100">
          Results for "<span class="text-gray-400">{{ query }}</span
          >"
        </h2>
        <span class="bg-gray-700 text-gray-300 px-3 py-1 rounded-full text-sm"
          >{{ results.length }} documents found</span
        >
      </div>

      <div
        v-for="(result, index) in results"
        :key="index"
        class="bg-gray-800 rounded-lg border border-gray-700 hover:border-gray-600 hover:shadow-md transition-all duration-300 group"
      >
        <div class="p-6">
          <div class="flex justify-between items-start">
            <h3
              class="text-xl font-semibold text-gray-100 group-hover:text-gray-300 transition-colors mb-2"
            >
              {{ result.document.title }}
            </h3>
            <span class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm">
              {{ (result.score * 100).toFixed(1) }}% match
            </span>
          </div>

          <div class="flex items-center text-sm text-gray-400 mb-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4 mr-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
            <span>{{ result.document.authors.join(', ') }}</span>

            <span class="mx-2">•</span>

            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4 mr-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            <span>{{ result.document.date }}</span>

            <span class="mx-2">•</span>

            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4 mr-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"
              />
            </svg>
            <span>{{ result.document.language || 'Unknown' }}</span>
          </div>

          <p class="text-gray-300 mb-4">{{ truncateText(result.document.abstract, 250) }}</p>

          <div class="flex flex-wrap gap-2 mb-4">
            <span
              v-for="(keyword, i) in result.document.keywords.slice(0, 5)"
              :key="i"
              class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm"
            >
              {{ keyword }}
            </span>
            <span v-if="result.document.keywords.length > 5" class="text-xs text-gray-500">
              +{{ result.document.keywords.length - 5 }} more
            </span>
          </div>

          <div class="flex flex-wrap gap-3">
            <router-link
              :to="`/document/${encodeURIComponent(result.document.id)}`"
              class="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-gray-200 rounded transition-colors flex items-center"
            >
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
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                />
              </svg>
              View Document
            </router-link>
            <button
              @click="findSimilar(result.document.id)"
              class="px-4 py-2 bg-transparent border border-gray-700 hover:bg-gray-700 text-gray-200 rounded transition-colors flex items-center"
            >
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
                  d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                />
              </svg>
              Find Similar
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="query && searchPerformed" class="bg-gray-800 rounded-lg border border-gray-700">
      <div class="p-8 text-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-16 w-16 mx-auto text-gray-600 mb-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <h3 class="text-xl font-semibold text-gray-100 mb-2">No results found</h3>
        <p class="text-gray-400 mb-6">No documents match your search query "{{ query }}"</p>
        <div class="flex justify-center">
          <button
            @click="clearSearch"
            class="px-4 py-2 bg-transparent border border-gray-700 hover:bg-gray-700 text-gray-200 rounded transition-colors"
          >
            Clear search
          </button>
        </div>
      </div>
    </div>

    <div v-else class="bg-gray-800 rounded-lg border border-gray-700">
      <div class="p-8 text-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-16 w-16 mx-auto text-gray-600 mb-4"
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
        <h3 class="text-xl font-semibold text-gray-100 mb-2">Start your search</h3>
        <p class="text-gray-400">Enter a search query to find relevant documents</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../services/api'
import SearchForm from '../components/SearchForm.vue'

const route = useRoute()
const router = useRouter()

const query = ref('')
const results = ref([])
const loading = ref(false)
const error = ref(null)
const searchPerformed = ref(false)
const topK = ref(10)

let initialQuery = null

watch(
  () => route.query,
  (newQuery) => {
    if (newQuery.q) {
      query.value = newQuery.q

      if (newQuery.top_k) {
        topK.value = parseInt(newQuery.top_k) || 10
      }

      performSearch(query.value)
    } else {
      results.value = []
      searchPerformed.value = false
    }
  },
  { deep: true },
)

const performSearch = async (searchQuery) => {
  if (!searchQuery) return

  query.value = searchQuery
  loading.value = true
  error.value = null

  try {
    console.log(`Searching for "${searchQuery}" with top-k=${topK.value}`)
    const data = await api.search(searchQuery, topK.value)

    console.log('Search response:', data)

    if (data && data.results) {
      results.value = data.results
      console.log(`Received ${results.value.length} results`)
    } else {
      results.value = []
      console.warn('No results array in response:', data)
    }

    searchPerformed.value = true
  } catch (err) {
    console.error('Search error:', err)
    error.value = err.message || 'An error occurred while searching'
    results.value = []
  } finally {
    loading.value = false
  }
}

const handleSearch = (searchParams) => {
  if (typeof searchParams === 'string') {
    router.push({ query: { q: searchParams, top_k: topK.value } })
  } else {
    topK.value = searchParams.topK
    router.push({ query: { q: searchParams.query, top_k: searchParams.topK } })
  }
}

const clearSearch = () => {
  router.push({ query: {} })
  query.value = ''
  results.value = []
  searchPerformed.value = false
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const findSimilar = (docId) => {
  if (!docId) {
    console.error('Cannot find similar documents: No document ID provided')
    return
  }

  console.log('Finding similar documents for ID:', docId)
  router.push(`/document/${encodeURIComponent(docId)}?showSimilar=true`)
}

onMounted(() => {
  if (route.query.q) {
    initialQuery = route.query.q
    query.value = initialQuery

    if (route.query.top_k) {
      topK.value = parseInt(route.query.top_k) || 10
    }

    performSearch(query.value)
  }
})
</script>

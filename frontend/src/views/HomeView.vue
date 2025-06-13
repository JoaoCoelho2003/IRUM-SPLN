<template>
  <div class="space-y-8 animate-fade-in">
    <!-- Hero Section -->
    <section
      class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700"
    >
      <div class="relative px-6 py-12 sm:px-12 sm:py-16 md:py-24 lg:px-16 lg:py-28">
        <div class="mx-auto max-w-3xl text-center">
          <h1 class="text-4xl font-bold tracking-tight text-white sm:text-5xl md:text-6xl">
            <span class="block">Discover Research</span>
            <span class="block mt-2 text-gray-300">With Intelligent Search</span>
          </h1>
          <p class="mx-auto mt-6 max-w-xl text-lg text-gray-300">
            Explore academic documents with our advanced information retrieval system. Find relevant
            research papers, articles, and publications with ease.
          </p>
          <div class="mt-10">
            <search-form @search="handleSearch" class="max-w-2xl mx-auto" />
          </div>
        </div>
      </div>

      <!-- Decorative elements -->
      <div class="absolute -top-24 -right-24 w-64 h-64 bg-gray-700/20 rounded-full blur-3xl"></div>
      <div
        class="absolute -bottom-24 -left-24 w-64 h-64 bg-gray-700/20 rounded-full blur-3xl"
      ></div>
    </section>

    <!-- Features Section -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div
        class="bg-gray-800 border border-gray-700 rounded-lg hover:border-gray-600 transition-all group"
      >
        <div class="p-6">
          <div
            class="w-12 h-12 rounded-lg bg-gray-700 flex items-center justify-center mb-4 group-hover:bg-gray-600 transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-gray-300"
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
          <h2
            class="text-xl font-semibold mb-2 text-white group-hover:text-gray-200 transition-colors"
          >
            Advanced Search
          </h2>
          <p class="text-gray-300 mb-4">
            Search through the document collection using natural language queries and find exactly
            what you need.
          </p>
          <router-link to="/search" class="inline-flex items-center text-gray-300 hover:text-white">
            Start searching
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4 ml-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </router-link>
        </div>
      </div>

      <div
        class="bg-gray-800 border border-gray-700 rounded-lg hover:border-gray-600 transition-all group"
      >
        <div class="p-6">
          <div
            class="w-12 h-12 rounded-lg bg-gray-700 flex items-center justify-center mb-4 group-hover:bg-gray-600 transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-gray-300"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              />
            </svg>
          </div>
          <h2
            class="text-xl font-semibold mb-2 text-white group-hover:text-gray-200 transition-colors"
          >
            Browse Collection
          </h2>
          <p class="text-gray-300 mb-4">
            Browse through the document collection page by page and discover new research materials.
          </p>
          <router-link to="/browse" class="inline-flex items-center text-gray-300 hover:text-white">
            Start browsing
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4 ml-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </router-link>
        </div>
      </div>

      <div
        class="bg-gray-800 border border-gray-700 rounded-lg hover:border-gray-600 transition-all group"
      >
        <div class="p-6">
          <div
            class="w-12 h-12 rounded-lg bg-gray-700 flex items-center justify-center mb-4 group-hover:bg-gray-600 transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-gray-300"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
          </div>
          <h2
            class="text-xl font-semibold mb-2 text-white group-hover:text-gray-200 transition-colors"
          >
            System Statistics
          </h2>
          <p class="text-gray-300 mb-4">
            View statistics about the document collection and system performance metrics.
          </p>
        </div>
      </div>
    </section>

    <!-- Recent Documents Section -->
    <section class="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
      <div class="flex justify-between items-center p-6 border-b border-gray-700">
        <h2 class="text-xl font-semibold text-white">Recent Documents</h2>
        <router-link to="/browse" class="text-sm text-gray-300 hover:text-white"
          >View all</router-link
        >
      </div>
      <div class="p-6">
        <div v-if="loading" class="flex justify-center py-8">
          <div
            class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-400"
          ></div>
        </div>
        <div v-else-if="recentDocuments.length === 0" class="py-8 text-center">
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
          <p class="text-gray-400">No documents available</p>
        </div>
        <div v-else class="divide-y divide-gray-700">
          <div
            v-for="(doc, index) in recentDocuments"
            :key="index"
            class="py-4 first:pt-0 last:pb-0 hover:bg-gray-700/30 px-4 -mx-4 rounded-lg transition-colors"
          >
            <h3 class="text-lg font-medium text-white mb-1">{{ doc.title }}</h3>
            <p class="text-sm text-gray-400 mb-2">{{ doc.authors.join(', ') }} · {{ doc.date }}</p>
            <p class="text-gray-300 mb-3 line-clamp-2">{{ doc.abstract }}</p>
            <div class="flex justify-between items-center">
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="(keyword, i) in doc.keywords.slice(0, 3)"
                  :key="i"
                  class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm"
                >
                  {{ keyword }}
                </span>
              </div>
              <router-link
                :to="`/document/${getDocumentIndex(doc)}`"
                class="text-gray-300 hover:text-white text-sm font-medium"
              >
                View details
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SearchForm from '../components/SearchForm.vue'
import { api } from '../services/api'

const router = useRouter()
const recentDocuments = ref([])
const loading = ref(true)

const handleSearch = (query) => {
  router.push({
    path: '/search',
    query: { q: query },
  })
}

const getDocumentIndex = (document) => {
  return document.id || document.title
}

onMounted(async () => {
  try {
    const data = await api.getDocuments(1, 5)
    recentDocuments.value = data.documents
  } catch (error) {
    console.error('Failed to load recent documents:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

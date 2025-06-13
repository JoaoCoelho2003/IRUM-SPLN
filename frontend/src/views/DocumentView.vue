<template>
  <div class="max-w-6xl mx-auto px-4 py-8 animate-fade-in">
    <div v-if="loading" class="flex flex-col items-center justify-center py-16">
      <div
        class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-gray-400 mb-4"
      ></div>
      <p class="text-gray-400">Loading document...</p>
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

    <div v-else-if="document" class="space-y-6">
      <div class="flex items-center">
        <button
          @click="goBack"
          class="flex items-center text-gray-400 hover:text-gray-200 transition-colors"
        >
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
              d="M10 19l-7-7m0 0l7-7m-7 7h18"
            />
          </svg>
          Back
        </button>
      </div>

      <div class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
        <div class="border-b border-gray-700 p-6">
          <h1 class="text-2xl font-bold text-gray-100">{{ document.title }}</h1>
        </div>

        <div class="p-6">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Main content -->
            <div class="lg:col-span-2 space-y-6">
              <div>
                <h2 class="text-lg font-semibold text-gray-100 mb-3 flex items-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 mr-2 text-gray-400"
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
                  Abstract
                </h2>
                <div class="bg-gray-900 rounded-lg p-4 border border-gray-700">
                  <p class="text-gray-300 whitespace-pre-line">{{ document.abstract }}</p>
                </div>
              </div>

              <div>
                <h2 class="text-lg font-semibold text-gray-100 mb-3 flex items-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 mr-2 text-gray-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                    />
                  </svg>
                  Keywords
                </h2>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="(keyword, i) in document.keywords"
                    :key="i"
                    class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm"
                  >
                    {{ keyword }}
                  </span>
                  <span v-if="document.keywords.length === 0" class="text-gray-500">
                    No keywords available
                  </span>
                </div>
              </div>

              <div v-if="document.collections && document.collections.length > 0">
                <h2 class="text-lg font-semibold text-gray-100 mb-3 flex items-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 mr-2 text-gray-400"
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
                  Collections
                </h2>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="(collection, i) in document.collections"
                    :key="i"
                    class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm"
                  >
                    {{ collection }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Sidebar -->
            <div class="space-y-6">
              <div class="bg-gray-900 rounded-lg p-4 border border-gray-700">
                <h2 class="text-lg font-semibold text-gray-100 mb-3 flex items-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 mr-2 text-gray-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  Document Info
                </h2>

                <div class="space-y-3">
                  <div>
                    <h3 class="text-sm font-medium text-gray-400">Authors</h3>
                    <p class="text-gray-200">{{ document.authors.join(', ') }}</p>
                  </div>

                  <div>
                    <h3 class="text-sm font-medium text-gray-400">Publication Date</h3>
                    <p class="text-gray-200">{{ document.date }}</p>
                  </div>

                  <div>
                    <h3 class="text-sm font-medium text-gray-400">Document Type</h3>
                    <p class="text-gray-200">{{ document.type || 'Not specified' }}</p>
                  </div>

                  <div>
                    <h3 class="text-sm font-medium text-gray-400">Language</h3>
                    <p class="text-gray-200">{{ document.language || 'Not specified' }}</p>
                  </div>
                </div>
              </div>

              <div class="bg-gray-900 rounded-lg p-4 border border-gray-700">
                <h2 class="text-lg font-semibold text-gray-100 mb-3 flex items-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 mr-2 text-gray-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                    />
                  </svg>
                  Actions
                </h2>

                <div class="space-y-3">
                  <button
                    @click="loadSimilarDocuments"
                    class="w-full py-2 px-4 bg-gray-700 hover:bg-gray-600 text-gray-200 rounded transition-colors flex items-center justify-center"
                  >
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
                        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                      />
                    </svg>
                    Find Similar Documents
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Similar Documents Section -->
      <div class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
        <div class="border-b border-gray-700 p-6 flex justify-between items-center">
          <h2 class="text-xl font-semibold text-gray-100 flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 mr-2 text-gray-400"
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
            Similar Documents
          </h2>
          <button
            @click="loadSimilarDocuments"
            class="text-gray-400 hover:text-gray-200 transition-colors"
            :disabled="loadingSimilar"
          >
            {{ loadingSimilar ? 'Loading...' : 'Refresh' }}
          </button>
        </div>

        <div v-if="loadingSimilar" class="flex justify-center py-12">
          <div
            class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-400"
          ></div>
        </div>

        <div v-else-if="similarError" class="p-4">
          <div class="bg-red-900/20 border border-red-800/50 text-red-200 px-4 py-3 rounded-lg">
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
              <p>{{ similarError }}</p>
            </div>
          </div>
        </div>

        <div v-else-if="similarDocuments.length > 0" class="divide-y divide-gray-700">
          <div
            v-for="(result, index) in similarDocuments"
            :key="index"
            class="p-6 hover:bg-gray-700/50 transition-colors"
          >
            <div class="flex justify-between items-start">
              <h3
                class="text-lg font-semibold text-gray-100 mb-1 hover:text-gray-300 transition-colors"
              >
                <router-link :to="`/document/${encodeURIComponent(result.document.id)}`">
                  {{ result.document.title }}
                </router-link>
              </h3>
              <span class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm">
                {{ (result.score * 100).toFixed(1) }}% match
              </span>
            </div>

            <div class="flex items-center text-sm text-gray-400 mb-2">
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
            </div>

            <p class="text-gray-300 mb-3">{{ truncateText(result.document.abstract, 150) }}</p>

            <div class="flex flex-wrap gap-2">
              <span
                v-for="(keyword, i) in result.document.keywords.slice(0, 3)"
                :key="i"
                class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm"
              >
                {{ keyword }}
              </span>
              <span v-if="result.document.keywords.length > 3" class="text-xs text-gray-500">
                +{{ result.document.keywords.length - 3 }} more
              </span>
            </div>
          </div>
        </div>

        <div v-else class="p-8 text-center">
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
          <h3 class="text-xl font-semibold text-gray-100 mb-2">No similar documents found</h3>
          <p class="text-gray-400">Try searching for other documents or topics</p>
        </div>
      </div>
    </div>

    <div v-else class="bg-gray-800 rounded-lg border border-gray-700 p-8 text-center">
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
      <h3 class="text-xl font-semibold text-gray-100 mb-2">Document not found</h3>
      <p class="text-gray-400 mb-6">
        The document you're looking for doesn't exist or has been removed
      </p>
      <router-link
        to="/browse"
        class="py-2 px-4 bg-gray-700 hover:bg-gray-600 text-gray-200 rounded transition-colors inline-block"
      >
        Browse Documents
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../services/api'

const route = useRoute()
const router = useRouter()

// Get the document ID from the route params
const docId = decodeURIComponent(route.params.id)

const document = ref(null)
const loading = ref(true)
const error = ref(null)

const similarDocuments = ref([])
const loadingSimilar = ref(false)
const similarError = ref(null)

const showSimilar = ref(false)

onMounted(() => {
  console.log('Document component mounted with ID:', docId)
  loadDocument()
})

watch(
  () => route.query.showSimilar,
  (newShowSimilar) => {
    showSimilar.value = newShowSimilar !== undefined
    if (showSimilar.value) {
      loadSimilarDocuments()
    }
  },
)

const loadDocument = async () => {
  loading.value = true
  error.value = null

  try {
    console.log('Loading document with ID:', docId)
    const data = await api.getDocument(docId)
    document.value = data.document
    console.log('Document loaded:', document.value)
  } catch (err) {
    console.error('Error loading document:', err)
    error.value = err.message || 'An error occurred while loading the document'
  } finally {
    loading.value = false
  }
}

const loadSimilarDocuments = async () => {
  loadingSimilar.value = true
  similarError.value = null

  try {
    console.log('Loading similar documents for ID:', docId)
    const data = await api.getSimilarDocuments(docId)
    similarDocuments.value = data.results
    console.log('Similar documents loaded:', similarDocuments.value)
  } catch (err) {
    console.error('Error loading similar documents:', err)
    similarError.value = err.message || 'An error occurred while loading similar documents'
  } finally {
    loadingSimilar.value = false
  }
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const goBack = () => {
  router.back()
}

if (route.query.showSimilar !== undefined) {
  showSimilar.value = true
  loadSimilarDocuments()
}
</script>

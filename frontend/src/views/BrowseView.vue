<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6 text-gray-100">Browse Documents</h1>

    <div v-if="loading" class="flex justify-center my-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-400"></div>
    </div>

    <div
      v-else-if="error"
      class="bg-red-900/20 border border-red-800/50 text-red-200 px-4 py-3 rounded-lg mb-6"
    >
      <p>{{ error }}</p>
    </div>

    <div v-else>
      <div class="bg-gray-800 rounded-lg border border-gray-700 p-6 mb-8">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-100">Documents ({{ pagination.total }})</h2>
          <div class="flex items-center space-x-2">
            <label for="per-page" class="text-sm text-gray-300">Per page:</label>
            <select
              id="per-page"
              v-model="perPage"
              class="bg-gray-700 border border-gray-600 rounded px-2 py-1 text-sm text-gray-200"
              @change="changePage(1)"
            >
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="20">20</option>
              <option value="50">50</option>
            </select>
          </div>
        </div>

        <div v-if="documents.length > 0" class="space-y-6">
          <div
            v-for="(doc, index) in documents"
            :key="index"
            class="border-b border-gray-700 pb-4 last:border-b-0 hover:bg-gray-700/30 px-4 -mx-4 rounded-lg transition-colors"
          >
            <h3 class="text-lg font-semibold mb-1 text-gray-100">{{ doc.title }}</h3>

            <p class="text-sm text-gray-400 mb-2">{{ doc.authors.join(', ') }} ({{ doc.date }})</p>

            <p class="mb-2 text-gray-300">{{ truncateText(doc.abstract, 150) }}</p>

            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="(keyword, i) in doc.keywords.slice(0, 3)"
                :key="i"
                class="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded"
              >
                {{ keyword }}
              </span>
              <span v-if="doc.keywords.length > 3" class="text-xs text-gray-500">
                +{{ doc.keywords.length - 3 }} more
              </span>
            </div>

            <div class="flex space-x-4">
              <router-link
                :to="`/document/${encodeURIComponent(doc.id)}`"
                class="text-gray-400 hover:text-gray-200 transition-colors"
              >
                View Document
              </router-link>
              <button
                @click="findSimilar(doc.id)"
                class="text-gray-400 hover:text-gray-200 transition-colors"
              >
                Find Similar
              </button>
            </div>
          </div>
        </div>

        <div v-else class="text-gray-400">No documents found</div>

        <div v-if="pagination.totalPages > 1" class="flex justify-center mt-6">
          <div class="flex space-x-2">
            <button
              @click="changePage(pagination.page - 1)"
              :disabled="pagination.page === 1"
              class="px-3 py-1 border rounded"
              :class="
                pagination.page === 1
                  ? 'text-gray-600 border-gray-700'
                  : 'text-gray-300 border-gray-600 hover:bg-gray-700'
              "
            >
              Previous
            </button>

            <button
              v-for="pageNum in displayedPages"
              :key="pageNum"
              @click="changePage(pageNum)"
              class="px-3 py-1 border rounded"
              :class="
                pageNum === pagination.page
                  ? 'bg-gray-600 text-gray-100 border-gray-500'
                  : 'text-gray-300 border-gray-600 hover:bg-gray-700'
              "
            >
              {{ pageNum }}
            </button>

            <button
              @click="changePage(pagination.page + 1)"
              :disabled="pagination.page === pagination.totalPages"
              class="px-3 py-1 border rounded"
              :class="
                pagination.page === pagination.totalPages
                  ? 'text-gray-600 border-gray-700'
                  : 'text-gray-300 border-gray-600 hover:bg-gray-700'
              "
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../services/api'

const route = useRoute()
const router = useRouter()

const documents = ref([])
const loading = ref(true)
const error = ref(null)

const pagination = ref({
  page: 1,
  perPage: 10,
  total: 0,
  totalPages: 1,
})

const perPage = ref(10)

const displayedPages = computed(() => {
  const current = pagination.value.page
  const total = pagination.value.totalPages
  const delta = 2

  const range = []
  for (let i = Math.max(1, current - delta); i <= Math.min(total, current + delta); i++) {
    range.push(i)
  }

  return range
})

const page = ref(parseInt(route.query.page) || 1)
const perPageParam = ref(parseInt(route.query.per_page) || 10)

const loadDocuments = async () => {
  loading.value = true
  error.value = null

  try {
    const data = await api.getDocuments(pagination.value.page, perPage.value)
    documents.value = data.documents
    pagination.value = {
      page: data.page,
      perPage: data.per_page,
      total: data.total,
      totalPages: data.total_pages,
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'An error occurred while loading documents'
  } finally {
    loading.value = false
  }
}

const changePage = (newPage) => {
  if (newPage < 1 || newPage > pagination.value.totalPages) return

  router.push({
    query: {
      page: newPage,
      per_page: perPage.value,
    },
  })
}

const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const findSimilar = (docId) => {
  router.push(`/document/${docId}?showSimilar=true`)
}

onMounted(() => {
  pagination.value.page = page.value
  perPage.value = perPageParam.value

  loadDocuments()
})

watch(
  () => route.query,
  (newQuery) => {
    const pageFromQuery = parseInt(newQuery.page) || 1
    const perPageFromQuery = parseInt(newQuery.per_page) || perPage.value

    if (pageFromQuery !== pagination.value.page || perPageFromQuery !== perPage.value) {
      pagination.value.page = pageFromQuery
      perPage.value = perPageFromQuery
      loadDocuments()
    }
  },
)

watch(perPage, () => {
  changePage(1)
})
</script>

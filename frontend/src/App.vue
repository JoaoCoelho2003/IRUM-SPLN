<template>
  <div class="min-h-screen flex flex-col bg-[#181926]">
    <header class="bg-gray-900 border-b border-gray-800 sticky top-0 z-10">
      <div class="container mx-auto px-4 py-3">
        <div class="flex justify-between items-center">
          <router-link to="/" class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-gray-800 flex items-center justify-center">
              <span class="text-white font-bold text-xl">IR</span>
            </div>
            <h1 class="text-xl font-bold text-white">IRUM</h1>
          </router-link>

          <nav class="hidden md:block">
            <ul class="flex space-x-1">
              <li>
                <router-link
                  to="/"
                  class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
                  :class="[
                    $route.path === '/'
                      ? 'bg-gray-800 text-white'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white',
                  ]"
                >
                  Home
                </router-link>
              </li>
              <li>
                <router-link
                  to="/search"
                  class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
                  :class="[
                    $route.path === '/search'
                      ? 'bg-gray-800 text-white'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white',
                  ]"
                >
                  Search
                </router-link>
              </li>
              <li>
                <router-link
                  to="/browse"
                  class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
                  :class="[
                    $route.path === '/browse'
                      ? 'bg-gray-800 text-white'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white',
                  ]"
                >
                  Browse
                </router-link>
              </li>
            </ul>
          </nav>

          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden text-gray-300 hover:text-white"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                v-if="mobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <div
        v-if="mobileMenuOpen"
        class="md:hidden bg-gray-900 border-t border-gray-800 animate-fade-in"
      >
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link
            to="/"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            :class="[
              $route.path === '/'
                ? 'bg-gray-800 text-white'
                : 'text-gray-300 hover:bg-gray-800 hover:text-white',
            ]"
            @click="mobileMenuOpen = false"
          >
            Home
          </router-link>
          <router-link
            to="/search"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            :class="[
              $route.path === '/search'
                ? 'bg-gray-800 text-white'
                : 'text-gray-300 hover:bg-gray-800 hover:text-white',
            ]"
            @click="mobileMenuOpen = false"
          >
            Search
          </router-link>
          <router-link
            to="/browse"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            :class="[
              $route.path === '/browse'
                ? 'bg-gray-800 text-white'
                : 'text-gray-300 hover:bg-gray-800 hover:text-white',
            ]"
            @click="mobileMenuOpen = false"
          >
            Browse
          </router-link>
          <router-link
            to="/stats"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            :class="[
              $route.path === '/stats'
                ? 'bg-gray-800 text-white'
                : 'text-gray-300 hover:bg-gray-800 hover:text-white',
            ]"
            @click="mobileMenuOpen = false"
          >
            Stats
          </router-link>
        </div>
      </div>
    </header>

    <main class="container mx-auto px-4 py-8 flex-grow">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="bg-gray-900 border-t border-gray-800 py-6">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="flex items-center gap-2 mb-4 md:mb-0">
            <div class="w-8 h-8 rounded-lg bg-gray-800 flex items-center justify-center">
              <span class="text-white font-bold text-sm">IR</span>
            </div>
            <p class="text-gray-400">IRUM &copy; {{ new Date().getFullYear() }}</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const mobileMenuOpen = ref(false)
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Add these global styles to ensure text is visible */
body {
  @apply bg-[#181926] text-gray-200;
}

.card {
  @apply bg-gray-800 border border-gray-700 rounded-lg overflow-hidden;
}

.card-header {
  @apply flex justify-between items-center p-6 border-b border-gray-700;
}

.card-body {
  @apply p-6;
}

.tag {
  @apply bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm;
}

.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors inline-flex items-center justify-center;
}

.btn-primary {
  @apply bg-gray-700 hover:bg-gray-600 text-white;
}

.btn-secondary {
  @apply bg-transparent border border-gray-700 hover:bg-gray-700 text-gray-300;
}

.btn-ghost {
  @apply bg-transparent hover:bg-gray-800 text-gray-400 hover:text-white;
}

.badge {
  @apply px-2 py-1 text-xs font-medium rounded-full;
}

.badge-primary {
  @apply bg-gray-700 text-gray-300;
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

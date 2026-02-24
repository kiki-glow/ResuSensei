<template>
  <nav class="sticky top-0 z-50 flex items-center justify-between px-6 py-3 bg-white/90 backdrop-blur-md border-b border-[#ede9fe] shadow-sm">

    <!-- Logo -->
    <RouterLink to="/" class="flex items-center gap-2">
      <img src="../assets/logo.png" alt="ResuSensei" class="h-10 transition-transform duration-300 hover:-translate-y-1" />
    </RouterLink>

    <!-- Desktop Nav -->
    <ul class="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
      <li v-for="item in navItems" :key="item.id">
        <button
          @click="scrollToSection(item.id)"
          class="relative py-1 hover:text-primary-700 transition-colors duration-200
                 after:absolute after:bottom-0 after:left-0 after:w-0 after:h-0.5
                 after:bg-primary-500 after:transition-all after:duration-300
                 hover:after:w-full"
        >
          {{ item.label }}
        </button>
      </li>
    </ul>

    <!-- Desktop CTA -->
    <div class="hidden md:block">
      <button
        @click="scrollToSection('upload')"
        class="px-5 py-2 rounded-full bg-primary-500 hover:bg-primary-700 text-white text-sm font-semibold shadow-sm transition-all duration-200 hover:shadow-md hover:-translate-y-0.5"
      >
        Try Now — It's Free
      </button>
    </div>

    <!-- Mobile toggle -->
    <button
      @click="mobileMenuOpen = !mobileMenuOpen"
      class="md:hidden p-2 rounded-lg text-gray-600 hover:bg-[#f5f3ff] transition"
      aria-label="Toggle menu"
    >
      <svg v-if="!mobileMenuOpen" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
      <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
      </svg>
    </button>

    <!-- Mobile Menu -->
    <Transition name="slide-down">
      <div
        v-if="mobileMenuOpen"
        class="absolute top-full left-0 w-full bg-white border-b border-[#ede9fe] shadow-lg md:hidden"
      >
        <ul class="flex flex-col p-4 gap-1">
          <li v-for="item in navItems" :key="item.id">
            <button
              @click="scrollToSection(item.id); mobileMenuOpen = false"
              class="w-full text-left px-4 py-2.5 rounded-lg text-gray-700 hover:bg-[#f5f3ff] hover:text-primary-700 transition text-sm font-medium"
            >
              {{ item.label }}
            </button>
          </li>
          <li class="mt-2 pt-2 border-t border-gray-100">
            <button
              @click="scrollToSection('upload'); mobileMenuOpen = false"
              class="w-full px-4 py-2.5 rounded-full bg-primary-500 text-white text-sm font-semibold hover:bg-primary-700 transition"
            >
              Try Now — It's Free
            </button>
          </li>
        </ul>
      </div>
    </Transition>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const mobileMenuOpen = ref(false)

const navItems = [
  { id: 'home',     label: 'Home' },
  { id: 'upload',   label: 'Resume Analysis' },
  { id: 'features', label: 'Features' },
  { id: 'contact',  label: 'Contact Us' },
]

const scrollToSection = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.25s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
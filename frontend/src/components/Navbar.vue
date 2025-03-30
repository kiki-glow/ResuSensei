<template>
  <nav class="relative flex items-center justify-between px-6 py-4 shadow-md bg-sky-200/50 text-gray-600">
    <!-- Logo -->
    <div class="flex items-center rounded-full pl-6 space-x-2">
      <RouterLink to="/">
        <img src="../assets/logo.png" alt="logo" class="h-12 mb-2 cursor-pointer transition-transform duration-500 hover:translate-y-2">
      </RouterLink>
    </div>

    <!-- Desktop Navigation -->
    <ul class="hidden md:flex md:items-center md:space-x-8 text-gray-700 md:!flex">
      <li>
        <button 
          @click="scrollToSection('home')" 
          class="text-gray-600 hover:text-gray-900 transition duration-300"
          active-class="text-sky-300 font-bold"
          exact
          >
          Home
        </button>
      </li>
        <li>
          <button 
            @click="scrollToSection('analysis')" 
            class="text-gray-600 hover:text-gray-900 transition duration-300"
            active-class="text-sky-300 font-bold"
            >
            Resume Analysis
          </button>
        </li>
        <li>
          <button 
            @click="scrollToSection('features')" 
            class="text-gray-600 hover:text-gray-900 transition duration-300"
            active-class="text-sky-300 font-bold">
            Features
          </button>
        </li>
        <li>
          <button 
            @click="scrollToSection('contact')" 
            class="text-gray-600 hover:text-gray-900 transition duration-300"
            active-class="text-sky-300 font-bold">
            Contact Us
          </button>
        </li>
    </ul>

    <!-- Desktop Try Now Button -->
    <div class="hidden md:block md:!block">
      <RouterLink 
        to="/login"
        class="rounded-full bg-sky-300/50 text-blue-900 hover:text-blue-500 transition duration-300 px-6 py-2"
      >
        Try Now
      </RouterLink>
    </div>

    <!-- Mobile Menu Toggle -->
    <div class="md:hidden">
      <button 
        @click="toggleMobileMenu"
        class="text-gray-700 text-2xl focus:outline-none"
      >
        {{ mobileMenuOpen ? '✖' : '☰' }}
      </button>
    </div>

    <!-- Mobile Menu -->
    <div 
      v-if="mobileMenuOpen"
      class="absolute top-full left-0 w-full bg-sky-100 shadow-md md:hidden z-50"
    >
      <ul class="flex flex-col space-y-4 p-6">
        <li>
          <button 
            @click="scrollToSection('home'); toggleMobileMenu()" 
            class="block py-2 hover:text-gray-900"
            exact
          >
          Home
        </button>
        </li>
        <li>
          <button 
            @click="scrollToSection('about'); toggleMobileMenu()" 
            class="block py-2 hover:text-gray-900"
            >
            Resume Analysis
          </button>
        </li>
        <li>
          <button 
            @click="scrollToSection('features'); toggleMobileMenu()" 
            class="block py-2 hover:text-gray-900"
            >
            Features
          </button>
        </li>
        <li>
          <button 
            @click="scrollToSection('contact'); toggleMobileMenu()" 
            class="block py-2 hover:text-gray-900"
            >
            Contact Us
          </button>
        </li>
        <li class="mt-4">
          <RouterLink 
            to="/login"
            class="block py-2 px-4 bg-sky-300/50 w-[120px] text-center rounded-full text-blue-900 hover:text-blue-500 transition"
            @click="toggleMobileMenu"
          >
            Try Now
          </RouterLink>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from 'vue-router';

const mobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const scrollToSection = (sectionId) => {
  const section = document.getElementById(sectionId);
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
};
</script>

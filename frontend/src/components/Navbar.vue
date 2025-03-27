<template>
  <nav class="relative flex items-center justify-between px-6 py-4 shadow-md bg-sky-200/50 text-gray-600">
    <div class="flex items-center rounded-full pl-6 space-x-2">
      <RouterLink to="/">
        <img src="../assets/logo.png" alt="logo" class="h-12 mb-2 cursor-pointer transition-transform duration-500 hover:translate-y-2">
      </RouterLink>
    </div>

    <ul class="hidden md:flex flex-row space-x-8 text-gray-700">
      <li>
        <RouterLink 
          to="/"
          class="text-gray-600 hover:text-gray-900 transition duration-300 ease-in-out transform"
          active-class="text-sky-300 font-bold"
          exact 
        >
          Home
        </RouterLink>
      </li>
      <li>
        <RouterLink 
          to="/about"
          class="text-gray-600 hover:text-gray-900 transition duration-300 ease-in-out transform"
          active-class="text-sky-300 font-bold"
        >
          About Us
        </RouterLink>
      </li>
      <li>
        <RouterLink 
          to="/features"
          class="text-gray-600 hover:text-gray-900 transition duration-300 ease-in-out transform"
          active-class="text-sky-300 font-bold"
        >
          Features
        </RouterLink>
      </li>
      <li>
        <RouterLink 
          to="/contact"
          class="text-gray-600 hover:text-gray-900 transition duration-300 ease-in-out transform"
          active-class="text-sky-300 font-bold"
        >
          Contact Us
        </RouterLink>
      </li>
    </ul>

    <button 
      class="md:block sm:rounded-2xl md:rounded-full bg-sky-300/50 text-white hover:text-white transition duration-300 px-4 py-2"
      id="try-now-btn"
    >
      <RouterLink to="/login" class="text-gray-100 hover:text-white transition duration-300">
        Try Now
      </RouterLink>
    </button>

    <!-- mobile hamburger menu toggle btn -->
    <div class="md:hidden">
      <button 
        @click="toggleMobileMenu"
        class="text-gray-700 text-2xl focus:outline-none" 
      >
        <span v-if="mobileMenuOpen">✖</span>
        <span v-else>☰</span>
      </button>
    </div>

    <!-- mobile menu -->
<!-- Mobile menu -->
<div 
  v-if="mobileMenuOpen"
  class="absolute top-full left-0 w-full bg-sky-100 shadow-md md:hidden z-50"
  id="mobile-menu"
  >
  <ul class="flex flex-col space-y-2 p-4 text-gray-600">
    <li>
      <RouterLink 
        to="/"
        class="hover:text-gray-900"
        active-class="text-sky-300 font-bold"
        exact
        @click="toggleMobileMenu"
      >
        Home
      </RouterLink>
    </li>
    <li>
      <RouterLink
        to="/about"
        class="hover:text-gray-700"
        @click="toggleMobileMenu" 
      >
        About Us
      </RouterLink>
    </li>
    <li>
      <RouterLink
        to="/features"
        class="hover:text-gray-700"
        @click="toggleMobileMenu" 
      >
        Features
      </RouterLink>
    </li>
    <li>
      <RouterLink 
        to="/contact"
        class="hover:text-gray-900"
        @click="toggleMobileMenu"
      >
        Contact Us
      </RouterLink>
    </li>
    <li>
      <RouterLink 
        to="/login"
        class="hover:text-gray-900"
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
</script>

<style scoped>
nav ul li a {
  color: inherit; /* Inherit the color from the parent element */
}

button {
  color: inherit; /* Inherit the color from the parent element */
}

button a {
  color: inherit; /* Ensure the RouterLink inside the button inherits the color */
}

/* Hide regular navbar items on small screens */
@media (max-width: 768px) {
  ul {
    display: none; /* Hide the regular navbar items */
  }

  /* Ensure the hamburger menu button is visible */
  .md\\:hidden + div {
    display: block; /* Show the container for the hamburger menu button */
  }

  .md\\:hidden button {
    display: inline-block; /* Show the hamburger menu button */
  }

  /* Hide the "Try Now" button on small screens */
  .md\\:block {
    display: none;
  }

  #mobile-menu {
    display: flex;
    flex-direction: column; /* Show the mobile menu */
  }

  #try-now-btn {
    display: none; /* Hide the "Try Now" button */
  }
}

/* Show regular navbar items on larger screens */
@media (min-width: 769px) {
  ul {
    display: flex; /* Show the regular navbar items */
  }

  .md\\:hidden {
    display: none; /* Hide the hamburger menu button */
  }

  .md\\:block {
    display: block !important; /* Show the "Try Now" button */
  }
}
</style>
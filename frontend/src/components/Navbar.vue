<template>
  <nav class="relative flex items-center justify-between px-6 py-4 shadow-md bg-sky-200/50 text-gray-600">
    <div class="flex items-center rounded-full pl-6 space-x-2">
      <RouterLink to="/">
        <img src="../assets/logo.png" alt="logo" class="h-12 mb-2 cursor-pointer transition-transform duration-500 hover:translate-y-2">
      </RouterLink>
    </div>

    <ul class="flex direction-row md:flex space-x-8 text-gray-700 sm:hidden">
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

    <button class="rounded-full bg-sky-300/50 text-white hover:text-white transition duration-300 px-4 py-2">
      <RouterLink to="/login" class="text-gray-100 hover:text-white transition duration-300">
        Try Now
      </RouterLink>
    </button>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router';
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
</style>
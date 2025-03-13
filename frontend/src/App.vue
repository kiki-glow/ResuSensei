<template>
  <div class="min-h-screen bg-lightGray w-full">
    <Navbar />
    <div class="mt-4 w-full container mx-auto max-w-full">
      <RouterView />
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
</script>

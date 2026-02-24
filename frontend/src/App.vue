<template>
  <div class="min-h-screen bg-sky-50/30 w-full">
    <Navbar />
    <div class="w-full">
      <RouterView />
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>
<template>
  <footer id="contact" class="bg-sky-200/50 text-gray-700 py-8 mt-16 border-t border-gray-700">
    <div class="container mx-auto px-6 lg:px-20 flex sm:flex-col md:flex-row justify-between md:gap-50 items-start md:items-start">
      
      <!-- Left Section: About and Social Media -->
      <div class="flex-1">
        <h3 class="text-lg font-bold text-gray-900">ResuSensei</h3>
        <p class="text-sm mt-2">
          Using advanced AI to help job seekers optimize their resumes and increase their chances of landing interviews.
        </p>
        
        <!-- Social Icons -->
        <div class="flex space-x-3 mt-4">
          <a href="https://github.com/kiki-glow" target="_blank" class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300 transition">
            <font-awesome-icon :icon="['fab', 'github']" class="text-xl" />
          </a>
          <a href="https://www.linkedin.com/in/yourprofile/" target="_blank" class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300 transition">
            <font-awesome-icon :icon="['fab', 'linkedin']" class="text-xl" />
          </a>
          <a href="https://www.instagram.com/yourprofile/" target="_blank" class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300 transition">
            <font-awesome-icon :icon="['fab', 'instagram']" class="text-xl" />
          </a>
          <a href="mailto:your-email@example.com" class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300 transition">
            <font-awesome-icon :icon="['fas', 'envelope']" class="text-xl" />
          </a>
        </div>
      </div>

      <!-- Middle Section: Contact -->
      <div class="flex-1 md:pl-20">
        <h4 class="text-lg font-bold text-gray-900">Contact Us</h4>
        <ul class="mt-2 space-y-2">
          <li><a class="text-gray-600 hover:text-gray-900 transition">kiki1703m@gmail.com</a></li>
          <li><a href="#" class="text-gray-600 hover:text-gray-900 transition">info@resusensei.com</a></li>
        </ul>
      </div>

      <!-- Right Section: Resources -->
      <div class="flex-1 items-end">
        <h4 class="text-lg font-bold text-gray-900">Resources</h4>
        <ul class="mt-2 space-y-2">
          <li><a href="#" class="text-gray-600 hover:text-gray-900 transition">Blog</a></li>
          <li><a href="#" class="text-gray-600 hover:text-gray-900 transition">Career Tips</a></li>
          <li><a href="#" class="text-gray-600 hover:text-gray-900 transition">Resume Templates</a></li>
          <li><a href="#" class="text-gray-600 hover:text-gray-900 transition">Help Center</a></li>
        </ul>
      </div>
    </div>

    <!-- Divider -->
    <hr class="my-6 border-gray-300 mx-6">

    <!-- Bottom Section -->
    <div class="container mx-auto px-6 lg:px-20 flex sm:flex-col md:flex-row items-center justify-between text-sm text-gray-500">
      <p>&copy; 2025 ResuSensei. All rights reserved.</p>

      <!-- Rotating Logo -->
      <img src="../assets/logo.png" alt="ResuSensei Logo" class="w-20 h-10 cursor-pointer transition-transform duration-500 hover:rotate-360">

      <ul class="flex space-x-4 mt-2 md:mt-0">
        <li><a href="#" class="text-gray-600 hover:text-gray-900 transition">Privacy Policy</a></li>
        <li><a href="#" class="text-gray-600 hover:text-gray-900 transition">Terms of Service</a></li>
        <li><a href="#" class="text-gray-600 hover:text-gray-900 transition">Cookie Policy</a></li>
      </ul>
    </div>
  </footer>
</template>

<script setup>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faGithub, faLinkedin, faInstagram } from '@fortawesome/free-brands-svg-icons';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faGithub, faLinkedin, faInstagram, faEnvelope);
</script>

<style scoped>
/* Logo Rotation Effect */
img:hover {
  transform: rotate(360deg);
  transition: transform 0.5s ease-in-out;
}

/* Highlighted modifications */
@media (max-width: 768px) {
  .container {
    flex-direction: column;
    text-align: center;
  }

  .container > div, .container > ul {
    margin-bottom: 1rem;
  }

  .container > ul {
    justify-content: center;
  }
}
</style>
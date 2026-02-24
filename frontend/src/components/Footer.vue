<template>
  <footer id="contact" class="bg-white border-t border-indigo-100 pt-14 pb-8 mt-0">
    <div class="max-w-6xl mx-auto px-6">

      <!-- Top grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">

        <!-- Brand -->
        <div class="lg:col-span-2">
          <div class="flex items-center gap-2 mb-3">
            <img src="../assets/logo.png" alt="ResuSensei" class="h-8" />
          </div>
          <p class="text-sm text-gray-500 leading-relaxed max-w-xs">
            Using advanced AI to help job seekers optimize their resumes and
            increase their chances of landing interviews.
          </p>
          <div class="flex gap-3 mt-5">
            <a
              v-for="social in socials"
              :key="social.label"
              :href="social.href"
              target="_blank"
              :aria-label="social.label"
              class="w-9 h-9 flex items-center justify-center rounded-full bg-indigo-50 hover:bg-indigo-100 text-brand-indigo transition-colors duration-200"
            >
              <font-awesome-icon :icon="social.icon" class="text-sm" />
            </a>
          </div>
        </div>

        <!-- Contact -->
        <div>
          <h4 class="text-sm font-bold text-gray-800 mb-4">Contact Us</h4>
          <ul class="space-y-2 text-sm text-gray-500">
            <li class="flex items-center gap-2">
              <font-awesome-icon :icon="['fas', 'envelope']" class="text-brand-indigo text-xs" />
              kiki1703m@gmail.com
            </li>
            <li class="flex items-center gap-2">
              <font-awesome-icon :icon="['fas', 'envelope']" class="text-brand-indigo text-xs" />
              info@resusensei.com
            </li>
          </ul>
        </div>

        <!-- Resources -->
        <div>
          <h4 class="text-sm font-bold text-gray-800 mb-4">Resources</h4>
          <ul class="space-y-2 text-sm">
            <li v-for="link in resourceLinks" :key="link">
              <a href="#" class="text-gray-500 hover:text-brand-indigo transition-colors duration-200">{{ link }}</a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom bar -->
      <div class="border-t border-gray-100 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-gray-400">
        <p>&copy; {{ new Date().getFullYear() }} ResuSensei. All rights reserved.</p>
        <div class="flex gap-5">
          <a v-for="link in legalLinks" :key="link" href="#" class="hover:text-brand-indigo transition-colors">{{ link }}</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { library } from '@fortawesome/fontawesome-svg-core'
import { faGithub, faLinkedin, faInstagram } from '@fortawesome/free-brands-svg-icons'
import { faEnvelope } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faGithub, faLinkedin, faInstagram, faEnvelope)

const socials = [
  { label: 'GitHub',    href: 'https://github.com/kiki-glow',               icon: ['fab', 'github'] },
  { label: 'LinkedIn',  href: 'https://www.linkedin.com/in/yourprofile/',    icon: ['fab', 'linkedin'] },
  { label: 'Instagram', href: 'https://www.instagram.com/yourprofile/',      icon: ['fab', 'instagram'] },
  { label: 'Email',     href: 'mailto:kiki1703m@gmail.com',                  icon: ['fas', 'envelope'] },
]

const resourceLinks = ['Blog', 'Career Tips', 'Resume Templates', 'Help Center']
const legalLinks    = ['Privacy Policy', 'Terms of Service', 'Cookie Policy']
</script>
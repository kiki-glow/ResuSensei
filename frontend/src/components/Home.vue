<template>
  <div class="home-container min-h-screen flex flex-col">
    <div class="flex flex-row gap-20 bg-sky-200/20 flex-grow">

      <!-- left section -->
      <div class="flex flex-col items-left ml-6 justify-between w-1/2 h-full border-r border-gray-300 mb-4 shadow mt-8">
        <!-- heading -->
        <h1 class="text-4xl font-bold text-primary leading-tight">Perfect Your Resume <br> with Precision</h1> <br>
        <p class="mt-4 text-lg text-gray-700 max-w-2xl text-left">
          ResuSensei uses advanced AI to analyze and enhance your resume, <br>
          maximizing your chances of landing your dream job.
        </p>

        <div class="flex flex-row mt-4 py-6 space-x-3">
          <button class="sm:rounded-2xl md:rounded-full bg-sky-300/50 text-black transition duration-300 px-4 py-2">Analyze Resume</button>

          <button class="sm:rounded-2xl md:rounded-full bg-sky-100/20 border-gray-700/50 border text-black px-4 py-2">Learn More</button>
        </div>

        <!-- features -->
        <div class="flex flex-row mt-2 py-6 space-x-3">
          <div class="flex items-center space-x-2">
            <font-awesome-icon :icon="['fas', 'chart-line']" class="text-sky-600 text-xl"/>
            <p class="text-gray-600 font-semibold">Smart Analysis</p>
          </div>

          <div class="flex items-center space-x-2">
            <font-awesome-icon :icon="['fas', 'clipboard-check']" class="text-green-600 text-xl"/>
            <p class="text-gray-600 font-semibold">ATS Optimization</p>
          </div>

          <div class="flex items-center space-x-2">
            <font-awesome-icon :icon="['fas', 'user-tie']" class="text-purple-600 text-xl"/>
            <p class="text-gray-600 font-semibold">Expert Advice</p>
          </div>
        </div>
      </div>
    
      <!-- resume preview -->
      <div class="flex flex-col flex-1 items-center justify-center w-1/2 h-[400px] bg-gradient-to-br from-sky-100 to-sky-200 rounded-lg shadow-md mt-8 mb-6">
        <font-awesome-icon :icon="['fas', 'file-alt']" class="text-gray-500 text-4xl opacity-70"/>
        <p class="text-gray-500 mt-2 text-sm">Resume preview will appear here...</p>
      </div>
    </div>

    <!-- Upload Resume -->
    <div class="flex flex-col items-center mt-8 flex-grow">
      <h1 class="text-2xl font-bold mb-4">Upload Your Resume</h1>
      <div class="border-dashed border-2 border-gray-400 rounded-lg p-6 w-1/2 text-center h-64 flex flex-col items-center justify-center">
        <p>Drag and drop your resume, or click to upload</p>

        <!-- hidden file input-->
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileUpload"
          class="hidden">
        <!-- browse files --> 
        <button 
          @click="triggerFileInput"
          class="sm:rounded-2xl md:rounded-full bg-sky-300/50 text-black transition duration-300 px-4 py-2 mt-4">
          Browse Files
        </button>

        <!-- display uploaded file name -->
         <p v-if="uploadedFileName" class="mt-2 text-gray-700 text-sm">
          Uploaded: {{ uploadedFileName }}
         </p>
      </div>
    </div>

    <!-- resume analysis results -->
     <div class="flex flex-col mt-6">
      <div class="title flex flex-col items-center justify-center">
        <h1 class="text-2xl font-bold mb-4">Resume Analysis Results</h1>
        <p class="text-lg text-gray-600">
          Based on our AI analysis, here's how your resume performs and how you can improve it
        </p>
      </div>
     </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import { faChartLine, faClipboardCheck, faUserTie, faFileAlt } from '@fortawesome/free-solid-svg-icons';

library.add(faChartLine, faClipboardCheck, faUserTie, faFileAlt)

// refs for file upload
const fileInput = ref(null);
const uploadedFileName = ref("");

// function to trigger file upload dialog
const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};

// function to handle file selection
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    uploadedFileName.value = file.name;
  }
};
</script>
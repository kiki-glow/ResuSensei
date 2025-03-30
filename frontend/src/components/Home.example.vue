<template>
    <div class="home-container min-h-screen flex flex-col bg-sky-200/20">
      <div id="home" class="flex flex-row gap-20 bg-sky-200/20 flex-grow">
  
        <!-- Left Section -->
        <div class="flex flex-col items-left ml-6 justify-between w-1/2 h-full border-r border-gray-300 mb-4 shadow mt-8">
          <h1 class="text-4xl font-bold text-primary leading-tight">Perfect Your Resume <br> with Precision</h1>
          <br>
          <p class="mt-4 text-lg text-gray-700 max-w-2xl text-left">
            ResuSensei uses advanced AI to analyze and enhance your resume, <br>
            maximizing your chances of landing your dream job.
          </p>
  
          <div class="flex flex-row mt-4 py-6 space-x-3">
            <button class="sm:rounded-2xl md:rounded-full bg-sky-300/50 text-black transition duration-300 px-4 py-2">
              Analyze Resume
            </button>
  
            <button class="sm:rounded-2xl md:rounded-full bg-sky-100/20 border-gray-700/50 border text-black px-4 py-2">
              Learn More
            </button>
          </div>
        </div>
  
        <!-- Resume Preview -->
        <div class="flex flex-col flex-1 items-center justify-center w-1/2 h-[400px] bg-gradient-to-br from-sky-100 to-sky-200 rounded-lg shadow-md mt-8 mb-6">
          <font-awesome-icon :icon="['fas', 'file-alt']" class="text-gray-500 text-4xl opacity-70"/>
          <p v-if="!uploadedFileName" class="text-gray-500 mt-2 text-sm">Resume preview will appear here...</p>
          <p v-if="uploadedFileName" class="text-gray-600 mt-2 text-sm">Uploaded: {{ uploadedFileName }}</p>
        </div>
      </div>
  
      <!-- Upload Resume -->
      <div id="features" class="flex flex-col items-center mt-8 flex-grow">
        <h1 class="text-2xl font-bold mb-4">Upload Your Resume</h1>
        <div class="border-dashed border-2 border-gray-400 rounded-lg p-6 w-1/2 text-center h-64 flex flex-col items-center justify-center">
          <p>Drag and drop your resume, or click to upload</p>
          <input type="file" ref="fileInput" @change="handleFileUpload" class="hidden">
          <button @click="triggerFileInput" class="sm:rounded-2xl md:rounded-full bg-sky-300/50 text-black transition duration-300 px-4 py-2 mt-4">
            Browse Files
          </button>
        </div>
      </div>
  
      <!-- Resume Analysis Results -->
      <div id="analysis" v-if="analysis" class="flex flex-col mt-6">
        <div class="title flex flex-col items-center justify-center">
          <h1 class="text-2xl font-bold mb-4">Resume Analysis Results</h1>
          <p class="text-lg text-gray-600">Based on our AI analysis, here's how your resume performs and how you can improve it.</p>
        </div>
  
        <div class="flex flex-row justify-between items-start gap-6 mt-6 px-8">
  
          <!-- Score Overview (Chart) -->
          <div class="bg-white p-6 rounded-lg shadow-md w-1/4 flex flex-col items-center relative">
            <h2 class="text-lg font-bold mb-2">Score Overview</h2>
            <div class="relative w-40 h-40 flex items-center justify-center">
              <canvas ref="doughnutChart" class="absolute"></canvas>
              <p class="absolute text-2xl font-bold text-blue-700">{{ analysis.ats_score }}%</p>
            </div>
          </div>
  
          <!-- Score Breakdown -->
          <div class="bg-white p-6 space-y-3 rounded-lg shadow-md w-1/3 text-center">
            <h2 class="text-lg font-bold mb-4">Breakdown</h2>
            <div v-for="(value, key) in analysis.breakdown" :key="key" class="w-full mt-4">
              <p class="text-sm font-semibold">{{ key }} <span class="float-right">{{ value }}%</span></p>
              <div class="w-full bg-gray-200 h-2 rounded-full">
                <div class="bg-sky-300 h-2 rounded-full" :style="{ width: value + '%' }"></div>
              </div>
            </div>
          </div>
  
          <!-- Recommendations -->
          <div class="bg-white p-6 rounded-lg shadow-md w-1/4">
            <h2 class="text-lg font-bold">Recommendations</h2>
            <ul class="list-disc pl-5 text-gray-700 mt-2">
              <li v-for="(rec, index) in analysis.recommendations" :key="index">{{ rec }}</li>
            </ul>
          </div>
  
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from "vue";
  import axios from "axios";
  import Chart from "chart.js/auto";
  import { library } from "@fortawesome/fontawesome-svg-core";
  import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
  import { faFileAlt } from "@fortawesome/free-solid-svg-icons";
  
  library.add(faFileAlt);
  
  const fileInput = ref(null);
  const uploadedFileName = ref("");
  const analysis = ref(null);
  const doughnutChart = ref(null);
  let myChart = null;
  
  const triggerFileInput = () => {
    fileInput.value.click();
  };
  
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
  
    uploadedFileName.value = file.name;
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const uploadResponse = await axios.post("http://127.0.0.1:5000/upload", formData);
      analysis.value = uploadResponse.data;
    } catch (error) {
      console.error("Error uploading resume:", error);
    }
  };
  
  // **Watch for analysis update and render chart**
  watch(analysis, (newValue) => {
    if (newValue && newValue.ats_score !== undefined) {
      setTimeout(() => renderChart(newValue.ats_score), 500);
    }
  });
  
  // **Render Doughnut Chart**
  const renderChart = (score) => {
    if (!doughnutChart.value) return;
  
    if (myChart) {
      myChart.destroy();
    }
  
    const ctx = doughnutChart.value.getContext("2d");
    if (!ctx) return;
  
    myChart = new Chart(ctx, {
      type: "doughnut",
      data: {
        datasets: [
          {
            data: [score, 100 - score],
            backgroundColor: ["#2563eb", "#e2e8f0"],
          },
        ],
      },
      options: {
        cutout: "70%",
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false },
        },
      },
    });
  };
  </script>
  
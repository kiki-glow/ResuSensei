<template>
  <div class="home-container min-h-screen flex flex-col bg-sky-200/20">
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
          Based on our AI analysis, here's how your resume performs and how you can improve it.
        </p>
      </div>
    </div>

    <!-- Score, Breakdown, and Recommendations -->
    <div class="flex flex-row justify-between items-start gap-6 mt-6 px-8">

      <!-- Score Overview -->
      <div class="bg-white p-6 rounded-lg shadow-md w-1/4">
        <h2 class="text-lg font-bold">Score Overview</h2>
        <canvas ref="doughnutChart" class="w-32 h-32"></canvas>
      </div>

      <!-- Score Breakdown (Centered) -->
      <div class="bg-white p-6 space-y-3 rounded-lg shadow-md w-1/3 text-center">
        <h2 class="text-lg font-bold mb-4">Breakdown</h2>

        <div class="w-full mt-4">
          <p class="text-sm font-semibold">ATS Compatibility 
            <span class="float-right">82%</span>
          </p>
          <div class="w-full bg-gray-200 h-2 rounded-full">
            <div class="bg-sky-300 h-2 rounded-full w-[82%]"></div>
          </div>
        </div>

        <div class="w-full mt-4">
          <p class="text-sm font-semibold">Content Quality 
            <span class="float-right">75%</span>
          </p>
          <div class="w-full bg-gray-200 h-2 rounded-full">
            <div class="bg-sky-300 h-2 rounded-full w-[75%]"></div>
          </div>
        </div>

        <div class="w-full mt-4">
          <p class="text-sm font-semibold">Format & Structure 
            <span class="float-right">88%</span>
          </p>
          <div class="w-full bg-gray-200 h-2 rounded-full">
            <div class="bg-sky-300 h-2 rounded-full w-[88%]"></div>
          </div>
        </div>
      </div>

      <!-- Recommendations -->
      <div class="bg-white p-6 rounded-lg shadow-md w-1/4">
        <h2 class="text-lg font-bold">Recommendations</h2>
        <p class="text-gray-600 mt-2">Based on our analysis, we recommend these key improvements:</p>
        <ul class="list-disc pl-5 text-gray-700 mt-2">
          <li>Add more measurable achievements with specific metrics</li>
          <li>Incorporate more industry-specific keywords</li>
          <li>Improve the professional summary for better first impression</li>
        </ul>
        <button 
        class="mt-4 bg-transparent border-solid border border-gray-400/50 text-black/75 px-3 py-2 rounded-full sm:rounded-lg w-full text-center"
        >
          View Detailed Report
        </button>
      </div>
    </div>

    <!-- Resume Insights Section -->
<div class="flex flex-row justify-between items-start gap-6 mt-6 px-8">

<!-- Key Strengths -->
<div class="bg-white p-6 rounded-lg shadow-md w-1/4">
  <h2 class="text-lg font-bold">✅ Key Strengths</h2>
  <ul class="list-disc pl-5 text-gray-700 mt-2 space-y-2">
    <li>Strong educational background</li>
    <li>Clear work history timeline</li>
    <li>Good technical skills representation</li>
    <li>Proper contact information placement</li>
  </ul>
</div>

<!-- Areas to Improve -->
<div class="bg-white p-6 rounded-lg shadow-md w-1/4">
  <h2 class="text-lg font-bold">⚠ Areas to Improve</h2>
  <ul class="list-disc pl-5 text-gray-700 mt-2 space-y-2">
    <li>Add more quantifiable achievements to strengthen impact</li>
    <li>Include relevant keywords for better ATS optimization</li>
    <li>Streamline work experience section for clarity</li>
    <li>Add a professional summary highlighting your value proposition</li>
  </ul>
</div>

<!-- Skills Analysis -->
<div class="bg-white p-6 rounded-lg shadow-md w-1/3">
  <h2 class="text-lg font-bold">⚡ Skills Analysis</h2>
  
  <!-- Skill: Technical Skills -->
  <p class="text-sm font-semibold mt-2">Technical Skills 
    <span class="float-right">85%</span>
  </p>
  <div class="w-full bg-gray-200 h-2 rounded-full">
    <div class="bg-blue-500 h-2 rounded-full w-[85%]"></div>
  </div>

  <!-- Skill: Experience Relevance -->
  <p class="text-sm font-semibold mt-4">Experience Relevance 
    <span class="float-right">73%</span>
  </p>
  <div class="w-full bg-gray-200 h-2 rounded-full">
    <div class="bg-blue-500 h-2 rounded-full w-[73%]"></div>
  </div>

  <!-- Skill: Key Achievements -->
  <p class="text-sm font-semibold mt-4">Key Achievements 
    <span class="float-right">68%</span>
  </p>
  <div class="w-full bg-gray-200 h-2 rounded-full">
    <div class="bg-blue-500 h-2 rounded-full w-[68%]"></div>
  </div>

  <!-- Skill: Education -->
  <p class="text-sm font-semibold mt-4">Education 
    <span class="float-right">90%</span>
  </p>
  <div class="w-full bg-gray-200 h-2 rounded-full">
    <div class="bg-blue-500 h-2 rounded-full w-[90%]"></div>
  </div>
</div>

</div>

<!-- Expert Tips and Resources -->
<div class="flex flex-row justify-between items-start gap-6 mt-6 px-8">

<!-- Expert Tips -->
<div class="bg-white p-6 rounded-lg shadow-md w-1/3">
  <h2 class="text-lg font-bold">💡 Expert Tips</h2>
  <p class="text-gray-600 mt-2 italic">"Keep your resume concise and targeted. Most recruiters spend less than 10 seconds on initial review."</p>
  <p class="text-gray-600 mt-2 italic">"Use action verbs at the beginning of bullet points to create a stronger impact."</p>
</div>

<!-- Resources -->
<div class="bg-white p-6 rounded-lg shadow-md w-1/3">
  <h2 class="text-lg font-bold">📚 Resources</h2>
  <ul class="mt-2 space-y-2">
    <li><a href="#" class="text-blue-500 hover:underline">Resume Writing Guide</a></li>
    <li><a href="#" class="text-blue-500 hover:underline">ATS Optimization Tips</a></li>
    <li><a href="#" class="text-blue-500 hover:underline">Interview Preparation</a></li>
  </ul>
</div>

</div>

  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faChartLine, faClipboardCheck, faUserTie, faFileAlt } from "@fortawesome/free-solid-svg-icons";
import Chart from "chart.js/auto";

library.add(faChartLine, faClipboardCheck, faUserTie, faFileAlt);

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

// ✅ refs for the chart
const doughnutChart = ref(null);
let myChart = null; // Store chart instance

onMounted(() => {
  if (doughnutChart.value) {
    // Destroy previous chart instance if it exists
    if (myChart) {
      myChart.destroy();
    }

    // ✅ Custom Plugin to Show the Score Inside the Chart
    const centerTextPlugin = {
      id: "centerText",
      beforeDraw(chart) {
        const { width, height } = chart;
        const ctx = chart.ctx;
        ctx.restore();
        
        const fontSize = (height / 10).toFixed(2);
        ctx.font = `${fontSize}px Arial`;
        ctx.textBaseline = "middle";

        const text = "78%"; // Displayed score
        const textX = Math.round((width - ctx.measureText(text).width) / 2);
        const textY = height / 2;

        ctx.fillStyle = "#2563eb"; // Blue text color
        ctx.fillText(text, textX, textY);
        ctx.save();
      },
    };

    myChart = new Chart(doughnutChart.value.getContext("2d"), {
      type: "doughnut",
      data: {
        labels: ["Score"],
        datasets: [
          {
            data: [78, 22], // 78% score
            backgroundColor: ["#2563eb", "#e2e8f0"], // Blue and Gray
            borderWidth: 0,
          },
        ],
      },
      options: {
        cutout: "70%", // Donut effect
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false },
        },
      },
      plugins: [centerTextPlugin], // ✅ Register the custom plugin
    });
  }
});
</script>

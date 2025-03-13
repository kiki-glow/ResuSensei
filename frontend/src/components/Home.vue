<template>
  <div class="home-container min-h-screen flex flex-col">
    <div class="flex flex-row gap-20 bg-sky-200/20 flex-grow">
      <div class="flex flex-col items-left ml-6 justify-between w-1/2 h-full border-r border-gray-300">
        <h1 class="text-4xl font-bold text-primary">Perfect Your Resume <br> with Precision</h1> <br>
        <p class="mt-4 text-lg text-gray-700 max-w-2xl text-left">
          ResuSensei uses advanced AI to analyze and enhance your resume, <br>
          maximizing your chances of landing your dream job.
        </p>

        <div class="flex flex-row mt-4 py-6 space-x-3">
          <button class="md:rounded-full bg-sky-300/50 text-black transition duration-300 px-4 py-2">Analyze Resume</button>

          <button class="md:rounded-full bg-sky-100/20 border-gray-700/50 border-1 text-black px-4 py-2">Learn More</button>
        </div>
      </div>
    
      <!-- resume preview -->
      <div class="preview flex-1 bg-gray-100 w-1/2 h-full">
        <p placeholder="Your resume preview...">Your resume preview here...</p>
      </div>
    </div>

    <!-- Upload Resume -->
    <div class="flex flex-col items-center mt-8 flex-grow">
      <h1 class="text-2xl font-bold mb-4">Upload Your Resume</h1>
      <div class="border-dashed border-2 border-gray-400 rounded-lg p-6 w-1/2 text-center h-full">
        <p>Drag and drop your resume, or click to upload</p>
        <input type="file" id="resume" name="resume" class="hidden">
      </div>
    </div>
  </div>
</template>
  
<script setup>
</script>
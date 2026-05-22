<template>
  <div class="min-h-screen bg-gradient-to-b from-primary-50 to-white">

    <!-- ═══════════════════════════════════════════
         HERO SECTION
    ════════════════════════════════════════════ -->
    <section id="home" class="relative overflow-hidden px-6 pt-16 pb-20 md:pt-24 md:pb-28">
      <!-- Background blobs -->
      <div class="absolute -top-24 -right-24 w-96 h-96 bg-primary-200/40 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -bottom-16 -left-16 w-72 h-72 bg-primary-100/50 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative max-w-6xl mx-auto flex flex-col md:flex-row items-center gap-12">

        <!-- Left copy -->
        <div class="flex-1 text-center md:text-left">
          <span class="inline-block px-3 py-1 rounded-full bg-primary-100 text-brand-violet text-xs font-semibold tracking-wide mb-4">
            AI-Powered Resume Analysis
          </span>
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold text-gray-900 leading-tight">
            Perfect Your Resume<br>
            <span class="text-brand-indigo">with Precision</span>
          </h1>
          <p class="mt-5 text-lg text-gray-500 max-w-lg mx-auto md:mx-0">
            ResuSensei uses advanced AI to analyze and enhance your resume,
            maximizing your chances of landing your dream job.
          </p>

          <div class="flex flex-col sm:flex-row gap-3 mt-8 justify-center md:justify-start">
            <button
              @click="scrollTo('upload')"
              class="px-6 py-3 rounded-full bg-brand-purple hover:bg-brand-indigo text-white font-semibold shadow-md hover:shadow-lg transition-all duration-200 hover:-translate-y-0.5"
            >
              Analyze My Resume
            </button>
            <button
              @click="scrollTo('features')"
              class="px-6 py-3 rounded-full border border-gray-300 hover:border-primary-300 text-gray-600 hover:text-brand-violet font-semibold transition-all duration-200"
            >
              See How It Works
            </button>
          </div>

          <!-- Stats strip -->
          <div class="flex gap-8 mt-10 justify-center md:justify-start">
            <div v-for="stat in stats" :key="stat.label" class="text-center md:text-left">
              <p class="text-2xl font-bold text-brand-indigo">{{ stat.value }}</p>
              <p class="text-xs text-gray-400 mt-0.5">{{ stat.label }}</p>
            </div>
          </div>
        </div>

        <!-- Right — resume card mockup -->
        <div class="flex-1 w-full max-w-md">
          <div class="relative bg-white rounded-2xl shadow-xl border border-primary-100 p-6 mx-auto">
            <!-- Floating badge -->
            <div class="absolute -top-3 -right-3 bg-brand-purple text-white text-xs font-bold px-3 py-1 rounded-full shadow">
              ATS Ready ✓
            </div>

            <!-- Mock resume lines -->
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'user']" class="text-brand-purple text-lg" />
              </div>
              <div>
                <div class="h-3 w-28 bg-gray-200 rounded-full"></div>
                <div class="h-2 w-20 bg-gray-100 rounded-full mt-1.5"></div>
              </div>
            </div>
            <div class="space-y-2 mb-4">
              <div class="h-2 w-full bg-gray-100 rounded-full"></div>
              <div class="h-2 w-5/6 bg-gray-100 rounded-full"></div>
              <div class="h-2 w-4/6 bg-gray-100 rounded-full"></div>
            </div>
            <div class="border-t border-gray-100 pt-4 space-y-2">
              <div class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 rounded-full bg-brand-purple"></div>
                <div class="h-2 w-3/4 bg-gray-100 rounded-full"></div>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 rounded-full bg-brand-purple"></div>
                <div class="h-2 w-2/3 bg-gray-100 rounded-full"></div>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 rounded-full bg-brand-purple"></div>
                <div class="h-2 w-1/2 bg-gray-100 rounded-full"></div>
              </div>
            </div>

            <!-- Score badge -->
            <div class="mt-4 flex items-center justify-between bg-primary-50 rounded-xl p-3">
              <span class="text-xs font-semibold text-gray-500">ATS Score</span>
              <div class="flex items-center gap-2">
                <div class="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div class="h-full bg-brand-purple rounded-full" style="width: 82%"></div>
                </div>
                <span class="text-sm font-bold text-brand-violet">82%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════
         FEATURES STRIP
    ════════════════════════════════════════════ -->
    <section id="features" class="bg-white py-16 px-6">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900">Why ResuSensei?</h2>
          <p class="text-gray-500 mt-2">Everything you need to get past the ATS and into the interview.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="feature in features"
            :key="feature.title"
            class="group p-6 rounded-2xl border border-primary-100 hover:border-primary-300 hover:shadow-md bg-white transition-all duration-200"
          >
            <div class="w-11 h-11 rounded-xl bg-primary-100 group-hover:bg-primary-200 flex items-center justify-center mb-4 transition-colors">
              <font-awesome-icon :icon="feature.icon" class="text-brand-indigo text-lg" />
            </div>
            <h3 class="font-bold text-gray-800 mb-1">{{ feature.title }}</h3>
            <p class="text-sm text-gray-500 leading-relaxed">{{ feature.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════
         UPLOAD + ROLE SELECTOR
    ════════════════════════════════════════════ -->
    <section id="upload" class="py-16 px-6 bg-gradient-to-br from-primary-50 to-white">
      <div class="max-w-2xl mx-auto">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-gray-900">Upload Your Resume</h2>
          <p class="text-gray-500 mt-2">PDF, DOCX, or RTF — we'll handle the rest.</p>
        </div>

        <!-- Role selector -->
        <div class="mb-5">
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Target Role <span class="text-gray-400 font-normal">(optional but recommended)</span>
          </label>
          <select
            v-model="selectedRole"
            class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-brand-purple focus:ring-2 focus:ring-primary-100 outline-none text-sm text-gray-700 bg-white transition"
          >
            <option value="">— Select your target role —</option>
            <option v-for="role in availableRoles" :key="role.key" :value="role.key">
              {{ role.name }}
            </option>
          </select>
          <p v-if="rolesError" class="text-xs text-red-500 mt-1">{{ rolesError }}</p>
        </div>

        <!-- Drop zone -->
        <div
          @dragover.prevent="dragging = true"
          @dragleave="dragging = false"
          @drop.prevent="onDrop"
          @click="fileInput.click()"
          :class="[
            'relative border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-200',
            dragging
              ? 'border-brand-purple bg-primary-50 scale-[1.01]'
              : uploadedFile
                ? 'border-primary-300 bg-primary-50/50'
                : 'border-gray-300 hover:border-primary-300 hover:bg-primary-50/40 bg-white'
          ]"
        >
          <input
            ref="fileInput"
            type="file"
            accept=".pdf,.docx,.rtf"
            class="hidden"
            @change="onFileSelect"
          />

          <!-- Idle state -->
          <div v-if="!uploadedFile && !loading">
            <div class="w-14 h-14 rounded-full bg-primary-100 flex items-center justify-center mx-auto mb-4">
              <font-awesome-icon :icon="['fas', 'cloud-upload-alt']" class="text-brand-purple text-2xl" />
            </div>
            <p class="font-semibold text-gray-700">Drag & drop your resume here</p>
            <p class="text-sm text-gray-400 mt-1">or <span class="text-brand-indigo font-medium">browse files</span></p>
            <p class="text-xs text-gray-300 mt-3">PDF · DOCX · RTF · Max 10 MB</p>
          </div>

          <!-- File selected -->
          <div v-else-if="uploadedFile && !loading" class="flex items-center gap-4 justify-center">
            <div class="w-12 h-12 rounded-xl bg-primary-100 flex items-center justify-center shrink-0">
              <font-awesome-icon :icon="['fas', 'file-alt']" class="text-brand-indigo text-xl" />
            </div>
            <div class="text-left">
              <p class="font-semibold text-gray-800 text-sm truncate max-w-[200px]">{{ uploadedFile.name }}</p>
              <p class="text-xs text-gray-400 mt-0.5">{{ fileSize }}</p>
            </div>
            <button
              @click.stop="clearFile"
              class="ml-2 text-gray-300 hover:text-red-400 transition"
              title="Remove file"
            >
              <font-awesome-icon :icon="['fas', 'times-circle']" class="text-lg" />
            </button>
          </div>

          <!-- Uploading -->
          <div v-else class="flex flex-col items-center gap-3">
            <div class="w-14 h-14 rounded-full bg-primary-100 flex items-center justify-center mx-auto animate-pulse">
              <font-awesome-icon :icon="['fas', 'spinner']" class="text-brand-purple text-2xl fa-spin" />
            </div>
            <p class="font-semibold text-gray-700">Analyzing your resume…</p>
            <!-- Progress bar -->
            <div class="w-full max-w-xs bg-gray-200 rounded-full h-1.5 overflow-hidden">
              <div
                class="h-full bg-brand-purple rounded-full transition-all duration-300"
                :style="{ width: uploadProgress + '%' }"
              ></div>
            </div>
            <p class="text-xs text-gray-400">{{ uploadProgress }}%</p>
          </div>
        </div>

        <!-- Error -->
        <div v-if="apiError" class="mt-4 flex items-start gap-3 bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 text-sm">
          <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="mt-0.5 shrink-0" />
          <span>{{ apiError }}</span>
        </div>

        <!-- Submit -->
        <button
          @click="submitAnalysis"
          :disabled="!uploadedFile || loading"
          class="mt-5 w-full py-3.5 rounded-full bg-brand-purple hover:bg-brand-indigo disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold text-sm shadow-md hover:shadow-lg transition-all duration-200 hover:-translate-y-0.5"
        >
          <span v-if="!loading">
            <font-awesome-icon :icon="['fas', 'search']" class="mr-2" />
            Analyze Resume
          </span>
          <span v-else>Analyzing…</span>
        </button>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════
         RESULTS SECTION
    ════════════════════════════════════════════ -->
    <section id="analysis" v-if="analysis" class="py-16 px-6 bg-white">
      <div class="max-w-6xl mx-auto">

        <!-- Header -->
        <div class="text-center mb-10">
          <h2 class="text-3xl font-bold text-gray-900">Analysis Results</h2>
          <p class="text-gray-500 mt-2">
            Here's how your resume scores across 6 key dimensions.
          </p>
          <div v-if="analysis.target_role" class="inline-flex items-center gap-2 mt-3 px-4 py-1.5 bg-primary-50 border border-primary-200 rounded-full text-sm text-primary-700 font-medium">
            <font-awesome-icon :icon="['fas', 'crosshairs']" />
            Optimized for: {{ roleName(analysis.target_role) }}
          </div>
        </div>

        <!-- Top row: Score ring + Breakdown + Quick tips -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">

          <!-- Overall score ring -->
          <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-6 flex flex-col items-center justify-center">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Overall Score</h3>
            <div class="relative w-36 h-36">
              <svg class="w-full h-full -rotate-90" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" fill="none" stroke="#e0f2fe" stroke-width="12"/>
                <circle
                  cx="60" cy="60" r="50" fill="none"
                  :stroke="scoreColor(analysis.overall_score)"
                  stroke-width="12"
                  stroke-linecap="round"
                  :stroke-dasharray="`${analysis.overall_score * 3.14} 314`"
                  class="transition-all duration-1000"
                />
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-3xl font-extrabold" :class="scoreTextColor(analysis.overall_score)">
                  {{ analysis.overall_score }}
                </span>
                <span class="text-xs text-gray-400">out of 100</span>
              </div>
            </div>
            <div class="mt-4 px-4 py-1 rounded-full text-sm font-bold" :class="gradeBadgeClass(analysis.grade)">
              Grade {{ analysis.grade }}
            </div>
            <p class="text-xs text-gray-400 mt-2 text-center">{{ gradeLabel(analysis.grade) }}</p>
          </div>

          <!-- Score breakdown bars -->
          <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-6">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-5">Score Breakdown</h3>
            <div class="space-y-3.5">
              <div
                v-for="(value, key) in analysis.score_breakdown"
                :key="key"
              >
                <div class="flex justify-between text-xs font-medium text-gray-600 mb-1">
                  <span>{{ formatKey(key) }}</span>
                  <span :class="value >= 75 ? 'text-green-600' : value >= 50 ? 'text-yellow-600' : 'text-red-500'">
                    {{ value }}
                  </span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                  <div
                    class="h-full rounded-full transition-all duration-700"
                    :class="barColor(value)"
                    :style="{ width: value + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick tips -->
          <div class="bg-primary-50 rounded-2xl border border-primary-100 shadow-sm p-6">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Quick Tips</h3>
            <ul class="space-y-3">
              <li
                v-for="(tip, i) in analysis.quick_tips"
                :key="i"
                class="flex items-start gap-2 text-sm text-gray-700"
              >
                <span class="mt-0.5 shrink-0 text-base">{{ tip.split(' ')[0] }}</span>
                <span>{{ tip.split(' ').slice(1).join(' ') }}</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Role Analysis (if target role was selected) -->
        <div v-if="analysis.role_analysis" class="mb-6 grid grid-cols-1 md:grid-cols-2 gap-6">

          <!-- Keywords present -->
          <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-6">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4 flex items-center gap-2">
              <font-awesome-icon
                :icon="['fas', 'check-circle']"
                class="text-green-500"
              />
              Keywords Found
              <span class="ml-2 text-xs font-normal text-gray-400">
                ({{ analysis.role_analysis.essential_keywords.match_percentage }}% essential match)
              </span>
            </h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="kw in analysis.role_analysis.essential_keywords.present"
                :key="kw"
                class="px-2.5 py-1 rounded-full bg-green-50 border border-green-200 text-green-700 text-xs font-medium"
              >
                {{ kw }}
              </span>
              <span
                v-for="kw in analysis.role_analysis.preferred_keywords.present"
                :key="'p'+kw"
                class="px-2.5 py-1 rounded-full bg-primary-50 border border-primary-200 text-primary-700 text-xs font-medium"
              >
                {{ kw }}
              </span>
              <p v-if="!analysis.role_analysis.essential_keywords.present.length && !analysis.role_analysis.preferred_keywords.present.length"
                class="text-sm text-gray-400 italic">No role keywords detected yet.</p>
            </div>
          </div>

          <!-- Keywords missing -->
          <div class="bg-white rounded-2xl border border-red-100 shadow-sm p-6">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4 flex items-center gap-2">
              <font-awesome-icon
                :icon="['fas', 'triangle-exclamation']"
                class="text-yellow-500"
              />
              Missing Keywords
              <span class="ml-2 text-xs font-normal text-gray-400">Add these where relevant</span>
            </h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="kw in analysis.role_analysis.essential_keywords.missing.slice(0, 8)"
                :key="kw"
                class="px-2.5 py-1 rounded-full bg-red-50 border border-red-200 text-red-700 text-xs font-medium"
              >
                {{ kw }}
              </span>
              <span
                v-for="kw in analysis.role_analysis.preferred_keywords.missing.slice(0, 6)"
                :key="'pm'+kw"
                class="px-2.5 py-1 rounded-full bg-orange-50 border border-orange-200 text-orange-700 text-xs font-medium"
              >
                {{ kw }}
              </span>
            </div>
          </div>
        </div>

        <!-- Recommendations list -->
        <div class="bg-white rounded-2xl border border-primary-100 shadow-sm p-6">
          <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-5">
            Recommendations
            <span class="ml-2 text-xs font-normal text-gray-400">sorted by priority</span>
          </h3>

          <div class="space-y-3">
            <div
              v-for="(rec, i) in analysis.recommendations"
              :key="i"
              class="flex gap-4 p-4 rounded-xl border transition-all duration-150 hover:shadow-sm"
              :class="recBorderClass(rec.priority)"
            >
              <!-- Priority badge -->
              <div class="shrink-0 mt-0.5">
                <span
                  class="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide"
                  :class="recBadgeClass(rec.priority)"
                >
                  {{ rec.priority }}
                </span>
              </div>

              <!-- Content -->
              <div class="flex-1 min-w-0">
                <div class="flex items-start justify-between gap-2">
                  <p class="font-semibold text-gray-800 text-sm">{{ rec.title }}</p>
                  <span class="shrink-0 text-[10px] text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full whitespace-nowrap">
                    {{ rec.category }}
                  </span>
                </div>
                <p class="text-sm text-gray-500 mt-1 leading-relaxed">{{ rec.description }}</p>

                <!-- Keywords list -->
                <div v-if="rec.keywords?.length" class="flex flex-wrap gap-1.5 mt-2">
                  <span
                    v-for="kw in rec.keywords"
                    :key="kw"
                    class="px-2 py-0.5 bg-primary-50 border border-primary-200 text-primary-700 rounded-full text-[11px] font-medium"
                  >
                    {{ kw }}
                  </span>
                </div>

                <!-- Examples -->
                <div v-if="rec.examples?.length" class="mt-2 bg-gray-50 rounded-lg p-3 text-xs text-gray-500 space-y-0.5">
                  <p v-for="(ex, j) in rec.examples.filter(e => e)" :key="j">{{ ex }}</p>
                </div>

                <!-- Impact -->
                <p v-if="rec.impact" class="text-[11px] text-gray-400 mt-2 font-medium">
                  Impact: {{ rec.impact }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Re-analyze CTA -->
        <div class="text-center mt-8">
          <button
            @click="clearFile(); analysis = null; scrollTo('upload')"
            class="px-8 py-3 rounded-full border-2 border-primary-300 text-brand-violet font-semibold hover:bg-primary-50 transition-all duration-200"
          >
            <font-awesome-icon :icon="['fas', 'redo']" class="mr-2" />
            Analyze Another Resume
          </button>
        </div>

      </div>
    </section>

    <!-- ═══════════════════════════════════════════
         NEW: JOB BOARDS SECTION (PHASE 1)
    ════════════════════════════════════════════ -->
    <section 
      v-if="analysis" 
      class="py-12 px-6 bg-gradient-to-r from-green-50 via-emerald-50 to-teal-50"
    >
      <div class="max-w-6xl mx-auto">
        <div class="bg-white rounded-3xl shadow-xl p-8 md:p-12 border border-green-200">
          
          <!-- Header -->
          <div class="flex items-start gap-4 mb-8">
            <div class="w-16 h-16 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center shrink-0 shadow-lg">
              <font-awesome-icon :icon="['fas', 'briefcase']" class="text-white text-2xl" />
            </div>
            <div class="flex-1">
              <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                Ready to Apply?
              </h2>
              <p class="text-lg text-gray-600">
                Your resume scored <span class="font-bold text-green-600">{{ analysis.overall_score }}</span>! 
                Time to put it to work.
              </p>
            </div>
          </div>
 
          <!-- Job Boards Grid -->
          <div class="mb-8">
            <p class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">
              Find {{ roleName(analysis.target_role) }} jobs on:
            </p>
            
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <a 
                v-for="board in getJobBoards(analysis.target_role)" 
                :key="board.name"
                :href="board.url"
                target="_blank"
                rel="noopener noreferrer"
                class="group flex items-center gap-3 px-5 py-4 bg-white rounded-xl border-2 border-gray-200 hover:border-green-500 hover:shadow-lg transition-all duration-200"
              >
                <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center shrink-0 group-hover:bg-green-50 transition">
                  <font-awesome-icon :icon="board.icon" class="text-gray-600 group-hover:text-green-600 transition" />
                </div>
                <div class="flex-1 min-w-0">
                  <span class="font-semibold text-sm text-gray-900 group-hover:text-green-600 transition block truncate">
                    {{ board.name }}
                  </span>
                  <span class="text-xs text-gray-500">{{ board.subtitle }}</span>
                </div>
              </a>
            </div>
          </div>
 
          <!-- Success Story CTA -->
          <div class="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl p-6 border border-purple-200">
            <div class="flex items-center gap-3 mb-2">
              <font-awesome-icon :icon="['fas', 'star']" class="text-yellow-500 text-xl" />
              <h3 class="font-bold text-gray-900">Got an Interview or Job Offer?</h3>
            </div>
            <p class="text-sm text-gray-600 mb-3">
              Help others by sharing your success story! We'll feature it on our site.
            </p>
            <button 
              @click="showSuccessForm = true; scrollTo('success-form')"
              class="px-6 py-2.5 rounded-full bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold hover:shadow-lg transition-all duration-200 hover:-translate-y-0.5"
            >
              Share My Success Story
            </button>
          </div>
 
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════
         NEW: SUCCESS STORIES FORM (PHASE 1)
    ════════════════════════════════════════════ -->
    <section 
      id="success-form"
      v-if="showSuccessForm || successStories.length > 0"
      class="py-16 px-6 bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50"
    >
      <div class="max-w-3xl mx-auto">
        
        <!-- Success Form -->
        <div v-if="showSuccessForm" class="bg-white rounded-3xl shadow-2xl p-8 md:p-12 mb-12">
          <div class="text-center mb-8">
            <div class="w-20 h-20 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center mx-auto mb-4 shadow-lg">
              <font-awesome-icon :icon="['fas', 'trophy']" class="text-white text-3xl" />
            </div>
            <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
              <div class="flex items-center justify-center gap-2">
                <span>Share Your Success!</span>
                <font-awesome-icon 
                  :icon="['fas', 'star']"
                  class="text-yellow-400"
                />
              </div>
            </h2>
            <p class="text-gray-600 text-lg">
              Help others by sharing how ResuSensei helped you land your dream job
            </p>
          </div>
 
          <form @submit.prevent="submitSuccessStory" class="space-y-5">
            <!-- Name -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Your Name <span class="text-gray-400 font-normal">(or stay anonymous)</span>
              </label>
              <input 
                v-model="successForm.name" 
                type="text"
                placeholder="e.g., John D. or Anonymous"
                class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:ring-2 focus:ring-purple-100 outline-none transition"
                required
              />
            </div>
 
            <!-- Job Title -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Job Title You Got
              </label>
              <input 
                v-model="successForm.jobTitle" 
                type="text"
                placeholder="e.g., Senior Frontend Developer"
                class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:ring-2 focus:ring-purple-100 outline-none transition"
                required
              />
            </div>
 
            <!-- Company (optional) -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Company <span class="text-gray-400 font-normal">(optional)</span>
              </label>
              <input 
                v-model="successForm.company" 
                type="text"
                placeholder="e.g., Google, Microsoft, etc."
                class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:ring-2 focus:ring-purple-100 outline-none transition"
              />
            </div>
 
            <!-- Story -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Your Success Story <span class="text-gray-400 font-normal">(optional)</span>
              </label>
              <textarea 
                v-model="successForm.story"
                placeholder="How did ResuSensei help you? What changed in your resume that made the difference?"
                rows="5"
                class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:ring-2 focus:ring-purple-100 outline-none transition resize-none"
              ></textarea>
            </div>
 
            <!-- Before/After Score -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">
                  Score Before <span class="text-gray-400 font-normal">(optional)</span>
                </label>
                <input 
                  v-model.number="successForm.scoreBefore" 
                  type="number"
                  min="0"
                  max="100"
                  placeholder="e.g., 65"
                  class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:ring-2 focus:ring-purple-100 outline-none transition"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">
                  Score After <span class="text-gray-400 font-normal">(optional)</span>
                </label>
                <input 
                  v-model.number="successForm.scoreAfter" 
                  type="number"
                  min="0"
                  max="100"
                  placeholder="e.g., 85"
                  class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:ring-2 focus:ring-purple-100 outline-none transition"
                />
              </div>
            </div>
 
            <!-- Submit Button -->
            <div class="flex gap-3 pt-4">
              <button 
                type="submit"
                :disabled="submittingSuccess"
                class="flex-1 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-blue-600 text-white font-bold text-lg hover:shadow-xl transition-all duration-200 hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="!submittingSuccess">Submit Success Story</span>
                <span v-else>Submitting...</span>
              </button>
              <button 
                type="button"
                @click="showSuccessForm = false"
                class="px-6 py-4 rounded-xl border-2 border-gray-300 text-gray-700 font-semibold hover:bg-gray-50 transition"
              >
                Cancel
              </button>
            </div>
          </form>
 
          <!-- Success Message -->
          <div v-if="successSubmitted" class="mt-6 p-4 rounded-xl bg-green-50 border border-green-200 text-green-800 text-center">
            <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-600 mr-2" />
            Thank you! We'll review and feature your story soon! 
          </div>
        </div>
 
        <!-- Display Success Stories -->
        <div v-if="successStories.length > 0">
          <h2 class="text-3xl font-bold text-center text-gray-900 mb-8">
            Success Stories 
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div 
              v-for="story in successStories" 
              :key="story.id"
              class="bg-white rounded-2xl shadow-lg p-6 border border-purple-100 hover:shadow-xl transition"
            >
              <div class="flex items-start gap-3 mb-4">
                <div class="w-12 h-12 rounded-full bg-gradient-to-br from-purple-400 to-blue-500 flex items-center justify-center text-white font-bold text-lg shrink-0">
                  {{ story.name.charAt(0).toUpperCase() }}
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="font-bold text-gray-900">{{ story.name }}</h3>
                  <p class="text-sm text-gray-600">{{ story.jobTitle }}</p>
                  <p v-if="story.company" class="text-xs text-gray-500">at {{ story.company }}</p>
                </div>
                <div v-if="story.scoreAfter" class="text-right">
                  <div class="text-2xl font-bold text-green-600">{{ story.scoreAfter }}</div>
                  <div class="text-xs text-gray-500">Score</div>
                </div>
              </div>
              <p v-if="story.story" class="text-gray-700 text-sm leading-relaxed italic">
                "{{ story.story }}"
              </p>
            </div>
          </div>
        </div>
 
      </div>
    </section>
    
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faUser, faFileAlt, faCloudUploadAlt, faSearch, faSpinner,
  faTimesCircle, faExclamationCircle, faCrosshairs, faRedo,
  faBolt, faChartBar, faKey, faCheckCircle, faLayerGroup, faStar,
  faBriefcase, faTrophy  
} from '@fortawesome/free-solid-svg-icons'

library.add(
  faUser, faFileAlt, faCloudUploadAlt, faSearch, faSpinner,
  faTimesCircle, faExclamationCircle, faCrosshairs, faRedo,
  faBolt, faChartBar, faKey, faCheckCircle, faLayerGroup, faStar,
  faBriefcase, faTrophy  
)

// ── Constants 
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const stats = [
  { value: '10+',  label: 'Supported Roles' },
  { value: '6',    label: 'Score Dimensions' },
  { value: '100%', label: 'Free to Use' },
]

const features = [
  { icon: ['fas', 'bolt'],        title: 'Instant ATS Score',          desc: 'Get a real ATS compatibility score in seconds — not a vague "good" or "bad".' },
  { icon: ['fas', 'key'],         title: 'Keyword Gap Analysis',        desc: 'See exactly which keywords your target role requires and which ones are missing.' },
  { icon: ['fas', 'chart-bar'],   title: '6-Dimension Breakdown',       desc: 'Scores across ATS fit, content quality, structure, achievements, keywords & formatting.' },
  { icon: ['fas', 'crosshairs'],  title: 'Role-Specific Targeting',     desc: 'Tailored advice for 10+ roles: Frontend Dev, Data Analyst, Virtual Assistant & more.' },
  { icon: ['fas', 'check-circle'],title: 'Prioritized Recommendations', desc: 'Critical, High, Medium, Low — so you know exactly where to spend your effort first.' },
  { icon: ['fas', 'layer-group'], title: 'Multi-Format Support',        desc: 'Upload PDF, DOCX, or RTF — we extract and analyze text from all three.' },
]

// ── State 
const fileInput      = ref(null)
const uploadedFile   = ref(null)
const dragging       = ref(false)
const selectedRole   = ref('')
const availableRoles = ref([])
const rolesError     = ref('')
const loading        = ref(false)
const uploadProgress = ref(0)
const apiError       = ref('')
const analysis       = ref(null)

// NEW: Success form state
const showSuccessForm = ref(false)
const submittingSuccess = ref(false)
const successSubmitted = ref(false)
const successForm = ref({
  name: '',
  jobTitle: '',
  company: '',
  story: '',
  scoreBefore: null,
  scoreAfter: null
})

// NEW: Success stories list
const successStories = ref([])

// ── Computed 
const fileSize = computed(() => {
  if (!uploadedFile.value) return ''
  const mb = uploadedFile.value.size / 1_048_576
  return mb < 1 ? `${(mb * 1024).toFixed(0)} KB` : `${mb.toFixed(2)} MB`
})

// ── Lifecycle 
onMounted(async () => {
  try {
    const res = await axios.get(`${API_BASE}/api/roles`)
    availableRoles.value = res.data.available_roles
  } catch {
    rolesError.value = 'Could not load roles — is the backend running?'
  }
  
  // NEW: Load success stories
  await loadSuccessStories()
})

// ── Methods 
const scrollTo = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}

const onDrop = (e) => {
  dragging.value = false
  const f = e.dataTransfer.files[0]
  if (f) setFile(f)
}

const onFileSelect = (e) => {
  const f = e.target.files[0]
  if (f) setFile(f)
}

const setFile = (f) => {
  const allowed = ['application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword', 'text/rtf', 'application/rtf']
  const extOk = /\.(pdf|docx|rtf)$/i.test(f.name)
  if (!extOk) { apiError.value = 'Only PDF, DOCX, or RTF files are supported.'; return }
  if (f.size > 10 * 1024 * 1024) { apiError.value = 'File is too large (max 10 MB).'; return }
  uploadedFile.value = f
  apiError.value = ''
  analysis.value = null
}

const clearFile = () => {
  uploadedFile.value = null
  if (fileInput.value) fileInput.value.value = ''
  apiError.value = ''
  uploadProgress.value = 0
}

const submitAnalysis = async () => {
  if (!uploadedFile.value) return
  loading.value = true
  apiError.value = ''
  uploadProgress.value = 0
  analysis.value = null

  const form = new FormData()
  form.append('file', uploadedFile.value)
  if (selectedRole.value) form.append('target_role', selectedRole.value)

  try {
    const res = await axios.post(`${API_BASE}/api/analyze`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        uploadProgress.value = Math.round((e.loaded / e.total) * 100)
      },
    })
    analysis.value = res.data
    setTimeout(() => scrollTo('analysis'), 300)
  } catch (err) {
    apiError.value =
      err.response?.data?.error ||
      err.response?.data?.detail ||
      'Analysis failed. Please check the backend is running.'
  } finally {
    loading.value = false
  }
}

// NEW: Job boards configuration
const getJobBoards = (targetRole) => {
  const roleMap = {
    'frontend_developer': 'Frontend Developer',
    'backend_developer': 'Backend Developer',
    'full_stack_developer': 'Full Stack Developer',
    'data_analyst': 'Data Analyst',
    'data_scientist': 'Data Scientist',
    'devops_engineer': 'DevOps Engineer',
    'product_manager': 'Product Manager',
    'ui_ux_designer': 'UI/UX Designer',
    'virtual_assistant': 'Virtual Assistant',
    'cybersecurity_analyst': 'Cybersecurity Analyst'
  }
  
  const roleNameStr = roleMap[targetRole] || 'Software Engineer'
  const encodedRole = encodeURIComponent(roleNameStr)
  
  return [
    {
      name: 'LinkedIn',
      subtitle: 'Professional network',
      url: `https://www.linkedin.com/jobs/search/?keywords=${encodedRole}`,
      icon: ['fas', 'briefcase']
    },
    {
      name: 'Indeed',
      subtitle: 'Job search engine',
      url: `https://www.indeed.com/jobs?q=${encodedRole}`,
      icon: ['fas', 'briefcase']
    },
    {
      name: 'AngelList',
      subtitle: 'Startup jobs',
      url: `https://angel.co/jobs?q=${encodedRole}`,
      icon: ['fas', 'star']
    },
    {
      name: 'RemoteOK',
      subtitle: 'Remote positions',
      url: `https://remoteok.com/remote-${targetRole.replace('_', '-')}-jobs`,
      icon: ['fas', 'briefcase']
    },
    {
      name: 'We Work Remotely',
      subtitle: 'Remote jobs',
      url: `https://weworkremotely.com/remote-jobs/search?term=${encodedRole}`,
      icon: ['fas', 'briefcase']
    },
    {
      name: 'Glassdoor',
      subtitle: 'Reviews + jobs',
      url: `https://www.glassdoor.com/Job/jobs.htm?sc.keyword=${encodedRole}`,
      icon: ['fas', 'star']
    }
  ]
}

// NEW: Submit success story
const submitSuccessStory = async () => {
  submittingSuccess.value = true
  successSubmitted.value = false

  try {
    await axios.post(`${API_BASE}/api/success-story`, {
      name: successForm.value.name,
      job_title: successForm.value.jobTitle,
      company: successForm.value.company || null,
      story: successForm.value.story || null,
      score_before: successForm.value.scoreBefore || null,
      score_after: successForm.value.scoreAfter || null
    })

    successSubmitted.value = true
    
    // Reset form after 2 seconds
    setTimeout(() => {
      successForm.value = {
        name: '',
        jobTitle: '',
        company: '',
        story: '',
        scoreBefore: null,
        scoreAfter: null
      }
      showSuccessForm.value = false
      successSubmitted.value = false
    }, 2000)

  } catch (error) {
    console.error('Error submitting success story:', error)
    alert('Failed to submit. Please try again.')
  } finally {
    submittingSuccess.value = false
  }
}

// NEW: Load success stories
const loadSuccessStories = async () => {
  try {
    const response = await axios.get(`${API_BASE}/api/success-stories`)
    successStories.value = response.data.stories || []
  } catch (error) {
    console.error('Error loading success stories:', error)
  }
}

// ── Helpers 
const formatKey = (key) =>
  key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())

const roleName = (key) =>
  availableRoles.value.find(r => r.key === key)?.name || key

const scoreColor = (s) => s >= 80 ? '#22c55e' : s >= 60 ? '#3b82f6' : s >= 40 ? '#f59e0b' : '#ef4444'
const scoreTextColor = (s) => s >= 80 ? 'text-green-500' : s >= 60 ? 'text-brand-indigo' : s >= 40 ? 'text-yellow-500' : 'text-red-500'

const gradeBadgeClass = (g) => ({
  A: 'bg-green-100 text-green-700',
  B: 'bg-primary-100 text-primary-700',
  C: 'bg-yellow-100 text-yellow-700',
  D: 'bg-orange-100 text-orange-700',
  F: 'bg-red-100 text-red-700',
}[g] || 'bg-gray-100 text-gray-600')

const gradeLabel = (g) => ({
  A: 'Excellent — ATS-ready',
  B: 'Good — minor tweaks needed',
  C: 'Fair — several areas to improve',
  D: 'Poor — significant work needed',
  F: 'Needs a full rework',
}[g] || '')

const barColor = (v) =>
  v >= 75 ? 'bg-green-400' : v >= 50 ? 'bg-brand-purple' : v >= 30 ? 'bg-yellow-400' : 'bg-red-400'

const recBorderClass = (p) => ({
  critical: 'border-red-200   bg-red-50/30',
  high:     'border-orange-200 bg-orange-50/20',
  medium:   'border-yellow-200 bg-yellow-50/20',
  low:      'border-gray-200   bg-white',
}[p] || 'border-gray-200 bg-white')

const recBadgeClass = (p) => ({
  critical: 'bg-red-100 text-red-700',
  high:     'bg-orange-100 text-orange-700',
  medium:   'bg-yellow-100 text-yellow-700',
  low:      'bg-gray-100 text-gray-500',
}[p] || 'bg-gray-100 text-gray-500')
</script>
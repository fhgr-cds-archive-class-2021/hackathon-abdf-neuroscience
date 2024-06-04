<template>
  <div class="flex items-center justify-center gap-4 py-10">
    <select class="select select-bordered w-full max-w-xs" v-model="currentMood">
      <option v-if="!currentMood" disabled selected>Which mood do you want to be in?</option>
      <option v-for="mood in moods" :key="mood.mood" :value="mood.key">{{ mood.mood }}</option>
    </select>
    <button class="btn btn-circle btn-outline" @click="getSelectedMood">
      Play
    </button>
  </div>
  <div class="text-black">
    <ul>
      <li v-for="brainwave in currentBrainwaves" :key="brainwave">
        {{ brainwave.wave }}: {{ brainwave.value }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const moods = ref([
  { key: 0, mood: 'Happy' },
  { key: 1, mood: 'Sad' },
  { key: 2, mood: 'Angry' },
  { key: 3, mood: 'Excited' },
  { key: 4, mood: 'Calm' },
])

const currentMood = ref(null)

const currentBrainwaves = ref([
  { wave: 'alpha', value: 0 },
  { wave: 'beta', value: 0 },
  { wave: 'delta', value: 0 },
  { wave: 'theta', value: 0 },
  { wave: 'gamma', value: 0 },
])

const getSelectedMood = () => {
  axios.post('http://localhost:8000/target_brain_wave', { brain_wave: currentMood.value })
    .then(response => {
      console.log('Response:', response.data)
    })
    .catch(error => {
      console.error('Error:', error)
    })
}

setInterval(() => {
  // get api url /play every second
  axios.get('http://localhost:8000/play')
    .then(response => {
      console.log('Response:', response.data)
    })
    .catch(error => {
      console.error('Error:', error)
    })
  axios.get('http://localhost:8000/get_current_brain_waves')
    .then(response => {
      currentBrainwaves.value = JSON.parse(response.data)
    })
    .catch(error => {
      console.error('Error:', error)
    })
}, 1000)

</script>

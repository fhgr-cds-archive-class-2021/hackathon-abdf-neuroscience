<template>
  <div class="flex items-center justify-center gap-4 py-10">
    <select class="select select-bordered w-full max-w-xs" v-model="chosenMood">
      <option v-if="!chosenMood" disabled selected>Which mood do you want to be in?</option>
      <option v-for="mood in moods" :key="mood.mood" :value="mood.key">{{ mood.mood }}</option>
    </select>
    <button class="btn btn-circle btn-outline" @click="getSelectedMood">
      Play
    </button>
  </div>
  <div class="text-black flex flex-col w-screen text-center">
    <p><b>Your desired mood:</b> {{ chosenMood ? moods[chosenMood].mood : 'None' }}</p>
    <p><b>Your current mood:</b> {{ currentMood ? moods[currentMood].mood : 'None' }}</p>
  </div>
  <div class="text-black w-full flex justify-center items-center">
    <div class="my-10">
      <table class="table">
        <!-- head -->
        <thead>
          <tr>
            <th>Alpha</th>
            <th>Beta</th>
            <th>Gamma</th>
            <th>Delta</th>
            <th>Theta</th>
            <th>Sigma</th>
          </tr>
        </thead>
        <tbody>
          <!-- row 1 -->
          <tr>
            <td v-for = "brainwave in currentBrainwaves" :key="brainwave.wave">
              {{ brainwave.value.toFixed(2) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="flex justify-center">
    <apexchart width="500" type="bar" :options="options" :series="series"></apexchart>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import ApexCharts from 'apexcharts'
import VueApexCharts from 'vue-apexcharts'

const moods = ref([
  { key: 0, mood: 'Happy' },
  { key: 1, mood: 'Sad' },
  { key: 2, mood: 'Angry' },
  { key: 3, mood: 'Excited' },
  { key: 4, mood: 'Calm' },
  { key: 5, mood: 'Stressed' },
])

const chosenMood = ref(null)
const currentMood = ref(null)

const currentBrainwaves = ref([
  { wave: 'alpha', value: 0 },
  { wave: 'beta', value: 0 },
  { wave: 'delta', value: 0 },
  { wave: 'theta', value: 0 },
  { wave: 'gamma', value: 0 },
  { wave: 'sigma', value: 0 },
])

const options = ref({
  chart: {
    id: 'vuechart-example'
  },
  xaxis: {
    categories: ['Alpha', 'Beta', 'Gamma', 'Delta', 'Theta', 'Sigma']
  }
})

const series = computed(() => {
  return [{
    name: 'series-1',
    data: currentBrainwaves.value.map(brainwave => brainwave.value.toFixed(2))
  }]
})

const getSelectedMood = () => {
  axios.post('http://localhost:8000/target_brain_wave', { brainwave: chosenMood.value })
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

  axios.get('http://localhost:8000/get_current_mood')
    .then(response => {
      currentMood.value = JSON.parse(response.data)
    })
    .catch(error => {
      console.error('Error:', error)
    })
}, 1000)

</script>

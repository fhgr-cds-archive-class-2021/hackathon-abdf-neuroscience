<template>
  <div class="flex items-center justify-center h-screen gap-4">
    <select class="select select-bordered w-full max-w-xs">
      <option disabled selected>Which mood do you want to be in?</option>
      <option v-for="mood in moods" :key="mood.mood">{{ mood.mood }}</option>
    </select>
    <button class="btn btn-circle btn-outline" @click="getSelectedMood">
      Play
    </button>
  </div>
</template>

<script setup>

const moods = ref([
  { key: 'happy', mood: 'Happy' },
  { key: 'sad', mood: 'Sad' },
  { key: 'angry', mood: 'Angry' },
  { key: 'excited', mood: 'Excited' }
])

const getSelectedMood = () => {

  // Send the GET request with the selected mood
  fetch(`http://localhost:8000/`)
    .then(response => response.json())
    .then(data => {
      // Handle the response data from the server (optional)
      console.log("Mood response:", data);
    })
    .catch(error => {
      console.error("Error sending request:", error);
    });
}

</script>
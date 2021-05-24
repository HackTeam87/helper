<template>
  <div class="text-center">

    <v-overlay v-if="loader">
      <v-progress-circular
          :rotate="90"
          :size="100"
          :width="15"
          :value="value"
          color="primary"
      >
        {{ value }}
      </v-progress-circular>
    </v-overlay>
  </div>
</template>

<script>
export default {
  name: 'preloader',
  data() {
    return {
      interval: {},
      value: 0,
      loader: true,
    }
  },

  mounted() {
    this.interval = setInterval(() => {
      if (this.value === 100) {
        return (this.loader = false)
      }
      this.value += 20
    }, 600)
  },
}
</script>


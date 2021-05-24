<template>
  <div>
    <v-form v-on:submit.prevent="sendIP()">
      <v-card>
        <v-card-title>
          <v-spacer></v-spacer>
          <h2 style="color:#0275d8">Sw</h2>
          <v-spacer></v-spacer>
          <v-text-field
              v-model="search"
              label="Search"
              placeholder="10.1.1.11"
              hide-details
          >
          </v-text-field>
          <v-btn @click="sendIP()">show</v-btn>
        </v-card-title>
      </v-card>
    </v-form>
  </div>
</template>

<script>

export default {
  data() {
    return {
      search: '',
    }
  },
  methods: {
    sendIP() {
      if (this.search !== '') {
        this.$emit('setIp', this.search)
      }
    }
  },

}
</script>
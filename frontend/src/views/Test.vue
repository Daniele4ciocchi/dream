<template>
  <div>
    <h1>Test Component</h1>
    <p>Se vedi questo, Vue funziona!</p>
    <button @click="testAuth">Test Auth</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'TestComponent',
  data() {
    return {
      message: ''
    }
  },
  methods: {
    testAuth() {
      this.message = 'Auth test clicked!'
      console.log('Test auth clicked')
    }
  }
}
</script>

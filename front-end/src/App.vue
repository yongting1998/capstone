<template>
  <div id="app">
    <my-bus />
  </div>
</template>

<script>
import MyBus from "./components/MyBus.vue";

export default {
  name: "App",
  components: {
    MyBus,
  },
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  background: #2c2c2c;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>

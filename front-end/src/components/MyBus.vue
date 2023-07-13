<template>
  <section class="section">
    <h1>P411 Bus Prediction Model</h1>
    <div class="container">
      <h3>Bus Stop: {{ selectedBusStop }}</h3>
      <p v-if="time">{{ time }} mins</p>
      <div class="direction-button-wrapper">
        <button
          class="button--direction"
          :class="[selectedDirection == 1 ? 'active' : '']"
          @click="selectedDirection = 1"
        >
          Kulai to Larkin
        </button>
        <button
          class="button--direction"
          :class="[selectedDirection == 2 ? 'active' : '']"
          @click="selectedDirection = 2"
        >
          Larkin to Kulai
        </button>
      </div>
      <bus-stop-list
        :busStopList="KulaiToLarkinData"
        v-if="selectedDirection == 1"
        @selectedBusStop="selectBusStop"
      />
      <bus-stop-list
        :busStopList="LarkinToKulaiData"
        v-if="selectedDirection == 2"
        @selectedBusStop="selectBusStop"
      />
    </div>
  </section>
</template>

<script>
import KulaiToLarkin from "./KulaiToLarkin.json";
import LarkinToKulai from "./LarkinToKulai.json";
import BusStopList from "./BusStopList.vue";
export default {
  components: { BusStopList },
  data() {
    return {
      selectedDirection: 1,
      selectedBusStop: "",
      time: "",
      KulaiToLarkinData: KulaiToLarkin,
      LarkinToKulaiData: LarkinToKulai,
    };
  },
  methods: {
    selectBusStop(busStop) {
      this.selectedBusStop = busStop;
      this.getTiming();
    },
    getTiming() {
      fetch("http://127.0.0.1:105/")
        .then((response) => response.json())
        .then((data) => {
          console.log(data.time);
          this.time = data.time;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.section {
  min-height: 100vh;
  width: 100vw;
  background: #2c2c2c;
  color: rgb(233, 233, 233);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.container {
  margin-top: 50px;
  max-width: 1200px;
  height: 100%;
}
.button--direction {
  cursor: pointer;
  padding: 20px 40px;
  margin: 20px;
  border-radius: 8px;
  border: 2px solid rgb(233, 233, 233);
  color: rgb(233, 233, 233);
  background: transparent;
  box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
  &:hover {
    color: black;
    background: white;
  }
  &.active {
    color: black;
    background: white;
  }
}
</style>

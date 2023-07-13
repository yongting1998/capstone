<template>
  <div>
    <ul class="list--scroll">
      <li
        v-for="(busStop, index) in busStopList"
        :key="index"
        :id="`bustop${index}`"
        class="bus-stop-list-item"
        :class="{ active: isActive == index }"
        @click="selectBusStop(index, busStop)"
      >
        {{ busStop }}
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  props: ["busStopList"],
  data() {
    return {
      isActive: -1,
    };
  },
  methods: {
    selectBusStop(index, busStop) {
      this.$emit("selectedBusStop", busStop);
      this.isActive = index;
    },
  },
};
</script>
<style lang="scss" scoped>
.list--scroll {
  height: 50vh;
  overflow-y: scroll;
  cursor: pointer;
  width: 500px;
  border-top: 1px solid white;
  padding: 0;
}
.bus-stop-list-item {
  list-style-type: none;
  padding: 20px;
  border-bottom: 1px solid white;
  &:hover {
    color: rgb(0, 0, 0);
    background-color: rgb(185, 185, 185);
  }
  &.active {
    color: rgb(0, 0, 0);
    background-color: rgb(185, 185, 185);
  }
}
</style>

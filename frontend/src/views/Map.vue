<template>
  <div class="map">
    <NakamalMap></NakamalMap>
  </div>
</template>

<script>
import NakamalMap from '@/components/NakamalMap.vue';

export default {
  name: 'Map',
  components: {
    NakamalMap,
  },
};
</script>

<style>
html {
  overflow-y: auto;
}
</style>

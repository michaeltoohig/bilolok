<template>
  <div class="search">
    search
    <NakamalList />
  </div>
</template>

<script>
import NakamalList from '@/components/NakamalList.vue';

export default {
  name: 'Search',
  components: {
    NakamalList,
  },
  beforeMount() {
    this.$store.dispatch('nakamal/load');
  },
};
</script>

<style>

</style>

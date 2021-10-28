<template>
  <v-container>
    <v-row dense>
      <v-col cols="12" v-for="nakamal in nakamals" :key="nakamal.id">
        <nakamal-list-item :nakamal="nakamal"></nakamal-list-item>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn
          :disabled="!hasPrev"
          @click="page--"
        >
          Prev
        </v-btn>
        <v-btn
          :disabled="!hasNext"
          @click="page++"
        >
          Next
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import NakamalListItem from '@/components/NakamalListItem.vue';

export default {
  name: 'NakamalList',
  components: {
    NakamalListItem,
  },
  data() {
    return {
      page: 1,
      per_page: 8,
    };
  },
  computed: {
    ...mapGetters({
      allNakamals: 'nakamal/list',
      total: 'nakamal/total',
    }),
    start() {
      return this.end - this.per_page;
    },
    end() {
      return this.page * this.per_page;
    },
    hasNext() {
      return this.end < this.total;
    },
    hasPrev() {
      return this.start > 0;
    },
    nakamals() {
      const end = this.end > this.total ? this.total : this.end;
      const start = this.start < 0 ? 0 : this.start;
      return this.allNakamals.slice(start, end);
    },
  },
  methods: {
    ...mapActions({
      load: 'nakamal/load',
    }),
  },
  created() {
    if (this.total === 0) {
      this.load();
    }
  },
};
</script>

<style>

</style>

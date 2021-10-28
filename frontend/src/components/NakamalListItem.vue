<template>
  <v-card
    color="primary"
    dark
  >
    <v-card-title class="text-h5">
      {{ nakamal.name }}
    </v-card-title>

    <v-card-subtitle>Blah blah</v-card-subtitle>

    <v-card-actions>
      <v-btn text @click="viewPage(nakamal.id)">
        View Page
      </v-btn>
      <v-btn text @click="viewMap(nakamal.id)">
        View on Map
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'NakamalListItem',
  props: ['nakamal'],
  methods: {
    viewPage(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.$router.push({ name: 'Nakamal', params: { id } });
        });
    },
    viewMap(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.$router.push({ name: 'Map' });
        });
    },
  },
};
</script>

<style>

</style>

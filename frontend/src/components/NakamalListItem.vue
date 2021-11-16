<template>
  <v-card
    class="mx-auto"
    max-width="400"
  >
    <v-img
      v-if="nakamal.image"
      class="white--text align-end"
      height="200px"
      :src="nakamal.image.thumbnail"
    >
      <v-card-title></v-card-title>
    </v-img>

    <v-card-title class="pb-0">
      {{ nakamal.name }}
    </v-card-title>

    <v-card-text class="text--primary">
      <div>Location: {{ nakamal.lat }} S, {{ nakamal.lng }} E</div>

      <div>Somewhere in Vanuatu</div>
    </v-card-text>

    <v-card-actions>
      <v-btn
        text
        @click="viewPage(nakamal.id)"
        color="primary"
      >
        View Page
      </v-btn>
      <v-btn
        text
        @click="viewMap(nakamal.id)"
        color="primary"
      >
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

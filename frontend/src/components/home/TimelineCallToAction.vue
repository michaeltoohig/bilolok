<template>
  <div class="text-center">
    <v-icon x-large class="mb-3">mdi-dots-vertical</v-icon>
    <h2 class="headline text-h2">{{ $t('home.end_of_feed') }}</h2>
    <p>{{ $t('home.end_of_feed_extra') }}</p>
    <v-btn
      x-large
      tile
      color="primary"
      :to="{ name: 'Map' }"
    >
      {{ $t('home.go_to_map') }}
      <v-icon>mdi-chevron-right</v-icon>
    </v-btn>
  </div>
</template>

<script>
// import { defineComponent } from 'vue';

export default {};
</script>

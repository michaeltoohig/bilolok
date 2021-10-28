<template>
  <v-card
    tile
    flat
    color="grey lighten-4"
    class="mx-0"
  >
    <v-card-title>Basic Info!</v-card-title>
    <v-list class="transparent">
      <v-list-item>
        <v-list-item-title>Light</v-list-item-title>
        <v-list-item-subtitle>{{ nakamal.light }}</v-list-item-subtitle>
        <v-list-item-icon>
          <v-icon>mdi-lightbulb</v-icon>
        </v-list-item-icon>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>Owner</v-list-item-title>
        <v-list-item-subtitle>{{ nakamal.owner }}</v-list-item-subtitle>
        <v-list-item-icon>
          <v-icon>mdi-account</v-icon>
        </v-list-item-icon>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>Phone</v-list-item-title>
        <v-list-item-subtitle>{{ nakamal.phone }}</v-list-item-subtitle>
        <v-list-item-icon>
          <v-icon>mdi-phone</v-icon>
        </v-list-item-icon>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
export default {
  name: 'BasicInfoCard',
  props: ['nakamal'],
};
</script>

<style>

</style>

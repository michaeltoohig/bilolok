<template>
  <v-dialog
    v-model="showNearbyNakamals"
    persistent
    scrollable
    width="500"
    color="primary"
  >
    <v-card>
      <v-card-title >
        Nearby Kava Bars
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="py-3" v-if="nearbyNakamals.length > 0">
        <v-row dense>
          <v-col cols="12" v-for="nakamal in nearbyNakamals" :key="nakamal.id">
            <NakamalListItem
              :nakamal="nakamal"
              v-on:fly-to-nearby="flyToNearby"
            ></NakamalListItem>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-text v-else class="text-center mt-5 font-weight-bold h5">
        No kava bars nearby...
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          text
          @click="showNearbyNakamals = false"
        >
          close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {

}
</script>

<style>

</style>
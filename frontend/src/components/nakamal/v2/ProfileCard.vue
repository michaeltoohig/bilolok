<template>
  <v-card class="mb-3">
    <v-card-title class="d-flex flex-column justify-center text-center">
      <v-badge
        v-if="profile"
        :color="nakamal.lightBadge.color"
        :icon="nakamal.lightBadge.icon"
        overlap
        bordered
        left
        offset-x="35"
        offset-y="25"
        dark
      >
        <v-avatar
          size="164"
          class="mb-5 nakamal-avatar"
          v-ripple="{ center: true }"
        >
          <v-img
            :src="profile.thumbnail"
          ></v-img>
        </v-avatar>
      </v-badge>
      <h1 v-text="nakamal.name"></h1>
    </v-card-title>
  </v-card>
</template>

<script>
export default {
  props: {
    nakamal: {
      type: Object,
      required: true,
    },
    profile: {
      type: Object,
      required: false,
    },
  },
};
</script>

<style>
.nakamal-avatar {
  cursor: pointer;
}
</style>

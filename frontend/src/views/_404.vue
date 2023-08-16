<template>
  <v-container class="about">
    <v-responsive max-width="500" class="mx-auto text-center">
      <h1>
        404
        <template v-if="resource">
          {{ resource }}
        </template>
        Not Found
      </h1>
    </v-responsive>
  </v-container>
</template>

<script>
export default {
  name: 'not_found',
  props: {
    resource: {
      type: String,
      default: '',
    },
  },
};
</script>

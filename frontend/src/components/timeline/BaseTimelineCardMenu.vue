<template>
  <v-menu
    bottom
    left
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        icon
        v-bind="attrs"
        v-on="on"
      >
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </template>

    <v-list>
      <v-list-item @click.prevent="onShare">
        <v-list-item-icon>
          <v-icon>mdi-share-variant</v-icon>
        </v-list-item-icon>
        <v-list-item-title>
          {{ $t('buttons.share') }}
        </v-list-item-title>
      </v-list-item>
      <v-list-item v-if="userCanDelete" @click.prevent="onDelete">
        <v-list-item-icon>
          <v-icon>mdi-delete</v-icon>
        </v-list-item-icon>
        <v-list-item-title>
          {{ $t('buttons.delete') }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  name: 'BaseTimelineCardMenu',
  props: {
    onShare: {
      type: Function,
      required: true,
    },
    onDelete: {
      type: Function,
      required: true,
    },
    userCanDelete: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style>

</style>

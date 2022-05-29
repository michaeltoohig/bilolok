<template>
  <div>
    <v-card outlined>
      <v-card-text
        @click="selectCheckin"
        class="pb-0 d-flex flex-row"
      >
        <v-avatar
          class="mr-2 elevation-2"
          size="55"
          tile
        >
          <v-img :src="user.avatar"></v-img>
        </v-avatar>
        <v-textarea
          disabled
          filled
          counter
          maxlength="280"
          :label="$t('checkin.message_placeholder')"
          rows="1"
          row-height="30"
        ></v-textarea>
      </v-card-text>

      <v-card-actions>
        <v-btn
          style="display: none"
          color="primary"
        >
          <v-icon class="mr-2">mdi-video-plus</v-icon>
          Video
        </v-btn>
        <v-btn
          style="display: none"
          color="primary"
        >
          <v-icon class="mr-2">mdi-image-plus</v-icon>
          Image
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          color="secondary"
          @click="submitCheckin"
        >
          <v-icon class="mr-2">mdi-marker-check</v-icon>
          {{ $t('checkin.title') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'NakamalPost',
  emits: ['close-modal'],
  props: {
    nakamal: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      me: 'auth/user',
    }),
    user() {
      return this.$store.getters['user/find'](this.me.id);
    },
  },
  methods: {
    ...mapActions({
      checkin: 'checkin/add',
    }),
    submitCheckin() {
      this.checkin({ nakamal_id: this.nakamal.id, message: null });
    },
    close() {
      this.$emit('close-modal');
    },
    selectCheckin() {
      this.$emit('select-checkin');
    },
  },
};
</script>

<style>

</style>

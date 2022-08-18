<template>
  <v-dialog
    v-model="open"
    max-width="500"
    @click:outside="close"
  >
    <v-card>
      <v-card-title class="text-h5">
        {{ $t('checkin.title') }}
      </v-card-title>

      <v-card-text>
        <v-textarea
          ref="textarea"
          filled
          counter
          maxlength="280"
          :label="$t('checkin.message_placeholder')"
          rows="3"
          row-height="30"
          v-model="msg"
        ></v-textarea>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn
          text
          @click="close"
        >
          {{ $t('buttons.cancel') }}
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          text
          @click="submitCheckin"
        >
          {{ $t('buttons.submit') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'DialogCheckin',
  emits: ['close-modal'],
  props: {
    nakamal: {
      type: Object,
      required: true,
    },
    open: {
      type: Boolean,
      required: true,
      default: false,
    },
  },
  data() {
    return {
      msg: null,
    };
  },
  watch: {
    open(val) {
      if (val) {
        this.$nextTick(() => {
          this.$refs.textarea.focus();
        });
      }
    },
  },
  methods: {
    ...mapActions({
      checkin: 'checkin/add',
    }),
    submitCheckin() {
      this.close();
      this.checkin({ nakamal_id: this.nakamal.id, message: this.msg });
    },
    close() {
      this.$emit('close-modal');
    },
  },
};
</script>

<style>

</style>

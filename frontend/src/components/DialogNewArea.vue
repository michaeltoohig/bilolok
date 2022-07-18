<template>
  <v-dialog
    v-model="show"
    max-width="400"
  >
    <v-card>
      <v-card-title>{{ $t('nakamal.add_new_area') }}</v-card-title>
      <v-card-text>
        <p>{{ $t('nakamal.add_new_area_extra') }}</p>
      </v-card-text>
      <v-card-text>
        <v-text-field
          v-model="name"
          :label="$t('nakamal.attrs.area')"
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn
          @click="submit"
          text
          outlined
          color="primary"
        >
          {{ $t('buttons.submit') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import nakamalAreaApi from '@/api/nakamalAreas';

export default {
  name: 'DialogNewArea',
  inheritAttrs: false,
  props: {
    value: {
      type: Boolean,
    },
  },
  data() {
    return {
      name: null,
    };
  },
  computed: {
    isValid() {
      if (!this.name) return false;
      return true;
    },
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit('input', value);
      },
    },
  },
  methods: {
    async submit() {
      if (!this.isValid) return;
      const token = this.$store.getters['auth/token'];
      const data = await nakamalAreaApi.create(token, { name: this.name });
      this.$emit('submit', data);
      this.show = false;
    },
  },
};
</script>

<style>

</style>

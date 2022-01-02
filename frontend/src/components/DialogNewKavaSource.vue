<template>
  <v-dialog
    v-model="show"
    max-width="400"
  >
    <v-card>
      <v-card-title>Add New Kava Source</v-card-title>
      <v-card-text>
        <p>
          Specify the area/island and province of the kava.
          Please be sure a similar kava source does not already exist.
        </p>
      </v-card-text>
      <v-card-text>
        <v-text-field
          v-model="island"
          label="Island / Area"
        ></v-text-field>
        <v-select
          v-model="province"
          :items="provinces"
          label="Province"
        ></v-select>
      </v-card-text>
      <v-card-actions>
        <v-btn
          @click="submit"
          text
          outlined
          color="primary"
        >Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import nakamalKavaSourcesApi from '@/api/nakamalKavaSources';

export default {
  name: 'DialogNewKavasource',
  inheritAttrs: false,
  props: {
    value: {
      type: Boolean,
    },
  },
  data() {
    return {
      island: null,
      province: null,
      provinces: [
        'TORBA',
        'SANMA',
        'PENAMA',
        'MALAMPA',
        'SHEFA',
        'TAFEA',
      ],
    };
  },
  computed: {
    isValid() {
      if (!this.province) return false;
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
      const resp = await nakamalKavaSourcesApi.create(token, {
        island: this.island,
        province: this.province,
      });
      this.$emit('submit', resp.data);
      this.show = false;
    },
  },
};
</script>

<style>

</style>

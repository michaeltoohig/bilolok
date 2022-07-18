<template>
  <div>
    <v-select
      v-bind="$attrs"
      v-bind:value="value"
      @change="change"
      prepend-icon="mdi-plus-circle"
      @click:prepend="showNewDialog = !showNewDialog"
      :items="areas"
      item-value="id"
      item-text="name"
      :label="$t('nakamal.attrs.area')"
    ></v-select>
    <DialogNewArea
      v-model="showNewDialog"
      v-on:submit="addArea"
    ></DialogNewArea>
  </div>
</template>

<script>
import nakamalAreaApi from '@/api/nakamalAreas';
import DialogNewArea from '@/components/DialogNewArea.vue';

export default {
  name: 'SelectArea',
  inheritAttrs: false,
  props: ['value'],
  components: {
    DialogNewArea,
  },
  data() {
    return {
      showNewDialog: false,
      areas: [],
    };
  },
  methods: {
    change(value) {
      this.$emit('input', value);
    },
    addArea(area) {
      this.areas.unshift(area);
    },
    async getAreas() {
      this.areas = await nakamalAreaApi.getAll();
    },
  },
  async mounted() {
    await this.getAreas();
  },
};
</script>

<style>

</style>

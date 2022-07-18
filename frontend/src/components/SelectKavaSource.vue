<template>
  <div>
    <v-select
      v-bind="$attrs"
      v-bind:value="value"
      @change="change"
      prepend-icon="mdi-plus-circle"
      @click:prepend="showNewDialog = !showNewDialog"
      :items="kavaSources"
      item-value="id"
      item-text="name"
      :label="$t('nakamal.attrs.kava_source')"
    ></v-select>
    <DialogNewKavaSource
      v-model="showNewDialog"
      v-on:submit="addKavaSource"
    ></DialogNewKavaSource>
  </div>
</template>

<script>
import nakamalKavaSourcesApi from '@/api/nakamalKavaSources';
import DialogNewKavaSource from '@/components/DialogNewKavaSource.vue';

export default {
  name: 'SelectKavaSource',
  inheritAttrs: false,
  props: ['value'],
  components: {
    DialogNewKavaSource,
  },
  data() {
    return {
      rawKavaSources: [],
      showNewDialog: false,
    };
  },
  computed: {
    kavaSources() {
      /* eslint-disable arrow-body-style */
      return this.rawKavaSources.map((ks) => {
        let name = ks.province;
        if (ks.island) {
          name += `: ${ks.island}`;
        }
        return {
          id: ks.id,
          name,
        };
      }).sort((a, b) => {
        return (a.name < b.name) ? 1 : -1;
      });
    },
  },
  methods: {
    change(value) {
      this.$emit('input', value);
    },
    addKavaSource(ks) {
      this.rawKavaSources.push(ks);
    },
    async getKavaSources() {
      this.rawKavaSources = await nakamalKavaSourcesApi.getAll();
    },
  },
  async mounted() {
    await this.getKavaSources();
  },
};
</script>

<style>

</style>

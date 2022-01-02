<template>
  <v-select
    v-bind="$attrs"
    v-bind:value="value"
    @change="change"
    :items="items"
    label="Light Color"
  ></v-select>
</template>

<script>
export default {
  name: 'SelectLight',
  inheritAttrs: false,
  props: ['value'],
  data() {
    return {
      items: [
        'White',
        'Red',
        'Orange',
        'Yellow',
        'Green',
        'Blue',
        'Purple',
        'Pink',
        'Candle',
        'Hurricane Light',
        'None',
        'Other',
      ],
    };
  },
  methods: {
    change(value) {
      this.$emit('input', value);
    },
  },
};
</script>

<style>

</style>

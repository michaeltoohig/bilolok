<template>
  <v-container>
    <v-row v-if="!images.length">
      <v-col>
        <h2>No Images Yet</h2>
      </v-col>
    </v-row>
    <Photoswipe>
      <v-row>
        <v-col
          v-for="(image, i) in images"
          :key="i"
          class="d-flex flex-column child-flex"
          cols="4"
        >
          <img
            :data-image-id="image.id"
            v-pswp="image"
            :src="image.thumbnail"
            :lazy-src="image.msrc"
            :aspect-ratio="1"
            @contextmenu="show"
          />
        </v-col>
      </v-row>

      <v-menu
        v-model="showMenu"
        :position-x="x"
        :position-y="y"
        absolute
        offset-y
      >
        <v-list>
          <v-list-item link @click="removeImage">
            <v-list-item-title>Remove</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </Photoswipe>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';

export default {
  name: 'TabImages',
  components: {
  },
  props: ['nakamal'],
  data() {
    return {
      x: 0,
      y: 0,
      selectedImageId: null,
      showMenu: false,
    };
  },
  computed: {
    ...mapGetters({
      getImages: 'image/nakamal',
      getCheckins: 'checkin/nakamal',
    }),
    images() {
      return this.getImages(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
  },
  methods: {
    show(e) {
      e.preventDefault();
      this.showMenu = false;
      this.selectedImageId = e.target.getAttribute('data-image-id');
      this.x = e.clientX;
      this.y = e.clientY;
      this.$nextTick(() => {
        this.showMenu = true;
      });
    },
    removeImage() {
      /* eslint-disable no-alert, no-restricted-globals */
      if (confirm('Are you sure you want to remove this image?')) {
        this.$store.dispatch('image/remove', this.selectedImageId);
      }
    },
  },
};
</script>

<style>

</style>

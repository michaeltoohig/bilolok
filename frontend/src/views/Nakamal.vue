<template>
  <div class="nakamal">
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <v-card flat color="secondary">
        <v-card-title>
          <h1>{{ nakamal.name }}</h1>
        </v-card-title>
        <v-card-text>
          <ul class="list-unstyled">
            <li>Owner: {{ nakamal.owner }}</li>
            <li>Number: {{ nakamal.phone }}</li>
            <li>Light: {{ nakamal.light }}</li>
            <li>Checkins Today: {{ todayCheckins }}</li>
            <li>Checkins Month: {{ monthCheckins }}</li>
          </ul>
        </v-card-text>
        <v-card-actions>
          <v-btn
            text
            color="primary"
            @click="checkin({ nakamal_id: nakamal.id })"
          >
            Check-In
          </v-btn>
          <v-btn
            v-show="hasAdminAccess"
            text
            color="primary"
            :to="{ name: 'NakamalEdit', params: { id: nakamal.id } }"
          >
            Edit
          </v-btn>
          <v-btn
            v-show="hasAdminAccess"
            text
            color="error"
            @click="remove"
          >
            Remove
          </v-btn>
        </v-card-actions>
      </v-card>

      <!-- <v-container>
        <div v-if="checkins">
          <v-timeline
            align-top
            dense
          >
            <v-timeline-item
              v-for="checkin in checkins"
              :key="checkin.id"
              color="pink"
              small
            >
              <v-row class="pt-1">
                <v-col cols="3">
                  <strong>{{ checkin.created_at }}</strong>
                </v-col>
                <v-col>
                  <strong>{{ checkin.user_id }}</strong>
                  <div class="text-caption">
                    {{ checkin.message }}
                  </div>
                  <v-avatar>
                    <v-img
                      src="https://avataaars.io/?avatarStyle=Circle&topType=LongHairFrida&accessoriesType=Kurt&hairColor=Red&facialHairType=BeardLight&facialHairColor=BrownDark&clotheType=GraphicShirt&clotheColor=Gray01&graphicType=Skull&eyeType=Wink&eyebrowType=RaisedExcitedNatural&mouthType=Disbelief&skinColor=Brown"
                    ></v-img>
                  </v-avatar>
                  <v-avatar>
                    <v-img
                      src="https://avataaars.io/?avatarStyle=Circle&topType=ShortHairFrizzle&accessoriesType=Prescription02&hairColor=Black&facialHairType=MoustacheMagnum&facialHairColor=BrownDark&clotheType=BlazerSweater&clotheColor=Black&eyeType=Default&eyebrowType=FlatNatural&mouthType=Default&skinColor=Tanned"
                    ></v-img>
                  </v-avatar>
                </v-col>
              </v-row>
            </v-timeline-item>
          </v-timeline>
        </div>
        <div v-else>
          Be first to checkin
        </div>
      </v-container> -->

      <v-container>
        <v-tabs-items v-model="tab">
          <v-tab-item value="images">
            <v-container class="px-0">
              <v-row v-if="images.length === 0">
                <v-col>
                  <h2>No Images Yet</h2>
                </v-col>
              </v-row>
              <Photoswipe v-else>
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
          </v-tab-item>
        </v-tabs-items>
      </v-container>
    </div>

    <v-fab-transition>
      <v-btn
        :key="activeFab.icon"
        fixed
        fab
        large
        dark
        bottom
        right
        :color="activeFab.color"
        @click="activeFab.action"
      >
        <v-icon>{{ activeFab.icon }}</v-icon>
      </v-btn>
    </v-fab-transition>

    <NakamalImageUpload
      v-if="!loading"
      :nakamal="nakamal"
      :open="openUploadDialog"
      @close-modal="() => this.openUploadDialog = false"
    ></NakamalImageUpload>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import NakamalImageUpload from '@/components/NakamalProfile/NakamalImageUpload.vue';

export default {
  name: 'Nakamal',
  components: {
    NakamalImageUpload,
  },
  data() {
    return {
      tab: 'images',
      openUploadDialog: false,
      x: 0,
      y: 0,
      selectedImageId: null,
      showMenu: false,
    };
  },
  computed: {
    ...mapGetters({
      hasAdminAccess: 'auth/hasAdminAccess',
      nakamal: 'nakamal/selected',
      getImages: 'image/nakamal',
      getCheckins: 'checkin/nakamal',
      getTodayCheckins: 'checkin/countToday',
      getMonthCheckins: 'checkin/countMonth',
    }),
    images() {
      if (!this.nakamal) return [];
      return this.getImages(this.nakamal.id);
      // .sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
    },
    checkins() {
      if (!this.nakamal) return [];
      return this.getCheckins(this.nakamal.id);
    },
    todayCheckins() {
      if (!this.nakamal) return 0;
      return this.getTodayCheckins(this.nakamal.id);
    },
    monthCheckins() {
      if (!this.nakamal) return 0;
      return this.getMonthCheckins(this.nakamal.id);
    },
    loading() {
      return !this.nakamal;
    },
    activeFab() {
      switch (this.tab) {
        case 'timeline': return { color: 'success', icon: 'mdi-share-variant', action: () => {} };
        case 'images': return { color: 'red', icon: 'mdi-image-plus', action: () => { this.openUploadDialog = !this.openUploadDialog; } };
        default: return {};
      }
    },
  },
  methods: {
    ...mapActions({
      checkin: 'checkin/add',
    }),
    remove() {
      /* eslint-disable no-alert, no-restricted-globals */
      if (confirm('Are you sure you want to remove this nakamal?')) {
        this.$store.dispatch('nakamal/remove', this.nakamal.id)
          .then(() => {
            this.$router.push({ name: 'Home' });
          });
      }
    },
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
      if (confirm('Are you sure you want to remove this image?')) {
        this.$store.dispatch('image/remove', this.selectedImageId);
      }
    },
  },
  async mounted() {
    const { id } = this.$route.params;
    this.$store.dispatch('checkin/getNakamal', id);
    this.$store.dispatch('image/getNakamal', id);
    await this.$store.dispatch('nakamal/select', id)
      .then(() => {
        if (!this.nakamal) {
          this.$store.dispatch('nakamal/loadOne', id);
        }
      });
  },
};
</script>

<style>

</style>

<template>
  <div class="nakamal">
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <v-card flat color="secondary">
        <v-card-title>
          <h1>{{ user.id }}</h1>
        </v-card-title>
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
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Profile',
  data() {
    return {
    };
  },
  computed: {
    user() {
      return this.$store.getters['auth/user'];
    },
    ...mapGetters({
      hasAdminAccess: 'auth/hasAdminAccess',
      // nakamal: 'nakamal/selected',
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
    loading() {
      return !this.user;
    },
  },
  methods: {
    removeImage() {
      /* eslint-disable no-alert, no-restricted-globals */
      if (confirm('Are you sure you want to remove this image?')) {
        this.$store.dispatch('image/remove', this.selectedImageId);
      }
    },
  },
  async mounted() {
    await this.$store.dispatch('auth/getMe');
  },
};
</script>

<style>

</style>

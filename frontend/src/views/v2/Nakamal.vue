<template>
  <div class="nakamal">
      <v-container>
        <v-row>
          <v-col sm="4" cols="12">
            <v-card class="mb-3">
              <v-card-title class="d-flex flex-column justify-center text-center">
                <v-badge
                  v-if="nakamalProfile"
                  :color="nakamal.lightBadge.color"
                  :icon="nakamal.lightBadge.icon"
                  overlap
                  bordered
                  left
                  offset-x="35"
                  offset-y="25"
                  dark
                >
                  <v-avatar
                    size="164"
                    class="mb-5 nakamal-avatar"
                    v-ripple="{ center: true }"
                    @click="goToTabImages"
                  >
                    <v-img
                      :src="nakamalProfile.thumbnail"
                    ></v-img>
                  </v-avatar>
                </v-badge>
                <h1 v-text="nakamal.name"></h1>
              </v-card-title>
              <v-card-text class="px-3 pb-3">
                <v-alert
                  v-show="isFeatured"
                  color="accent"
                  outlined
                  icon="mdi-trophy-award"
                  border="left"
                  class="mx-0 mt-0 mb-1 py-2"
                >
                  {{ $t('nakamal.is_featured') }}
                </v-alert>
                <v-alert
                  v-show="hasRecentCheckin"
                  outlined
                  icon="mdi-marker-check"
                  border="left"
                  class="mx-0 mt-0 mb-1 py-2"
                >
                  {{ $t('nakamal.has_recent_checkins') }}
                </v-alert>
              </v-card-text>
            </v-card>
            <CardChief :nakamal="nakamal"></CardChief>
            <v-list
              dense
              class="elevation-2"
            >
              <v-list-item-group
                color="primary"
              >
                <v-list-item @click="$router.push({ name: 'Map' })">
                  <v-list-item-icon>
                    <v-icon>mdi-map</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ $t('nakamal.view_on_map') }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item :disabled="isFeatured" @click="updateFeatured(nakamal.id)">
                  <v-list-item-icon>
                    <v-icon>mdi-trophy-award</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ $t('nakamal.set_featured') }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item @click="onShare">
                  <v-list-item-icon>
                    <v-icon>mdi-share-variant</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ $t('buttons.share') }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-spacer v-show="isUserVerified"></v-spacer>
                <v-list-item color="primary lighten-2" v-show="isUserVerified" @click="onEdit">
                  <v-list-item-icon>
                    <v-icon>mdi-pencil</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ $t('buttons.edit') }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item color="primary lighten-2" v-show="hasAdminAccess" @click="onRemove">
                  <v-list-item-icon>
                    <v-icon>mdi-trash-can-outline</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ $t('buttons.delete') }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>
          <v-col sm="8" cols="12">
            <v-card>
              <v-tabs
                v-model="tab"
                color="primary lighten-2"
                background-color="transparent"
                :fixed-tabs="$vuetify.breakpoint.mdAndDown"
              >
                <v-tab href="#details">{{ $t('nakamal.tab_details') }}</v-tab>
                <v-tab href="#timeline">{{ $t('nakamal.tab_timeline') }}</v-tab>
                <v-tab href="#images">{{ $t('nakamal.tab_images') }}</v-tab>
              </v-tabs>

              <v-card-text id="tab-content">
                <v-tabs-items v-if="!loading" v-model="tab">
                  <v-tab-item value="details">
                    <TabDetails :nakamal="nakamal"></TabDetails>
                  </v-tab-item>
                  <v-tab-item value="timeline">
                    <TabTimeline
                      :nakamal="nakamal"
                      @select-checkin="() => this.showCheckinDialog = true"
                      @select-video="() => this.showUploadVideoDialog = true"
                    />
                  </v-tab-item>
                  <v-tab-item value="images">
                    <TabImages :nakamal="nakamal"/>
                  </v-tab-item>
                </v-tabs-items>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import NakamalImageUpload from '@/components/nakamal/NakamalImageUpload.vue';
import DialogCheckin from '@/components/nakamal/DialogCheckin.vue';
import TabDetails from '@/components/nakamal/TabDetails.vue';
import TabTimeline from '@/components/nakamal/TabTimeline.vue';
import TabImages from '@/components/nakamal/TabImages.vue';
import CardChief from '@/components/nakamal/CardChief.vue';
import VideoUploadDialog from '@/components/nakamal/VideoUploadDialog.vue';

export default {
  name: 'Nakamal2',
  // props: {
  //   nakamal: {
  //     type: Object,
  //     required: true,
  //   },
  // },
  components: {
    VideoUploadDialog,
    DialogCheckin,
    NakamalImageUpload,
    TabDetails,
    TabTimeline,
    TabImages,
    CardChief,
  },
  data() {
    return {
      // nakamalProfile: null,
    };
  },
  computed: {
    ...mapGetters({
      nakamal: 'nakamal2/selected',
      profile: 'image2/get',
    }),
    nakamalProfile() {
      return this.profile(this.nakamal.profile);
    },
  },
};
</script>

<style>
.nakamal-avatar {
  cursor: pointer;
}
</style>

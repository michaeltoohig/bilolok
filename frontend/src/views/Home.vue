<template>
  <div class="home px-3">
    <v-container>
      <v-row>
        <v-col>
          <h1 class="text-h1 text-center">Bilolok</h1>

          <p class="text-center">
            Bilolok means <strong>Kava</strong> in the local language of a small
            village on the east, south-east side of Malekula island in Vanuatu.
          </p>

          <hr class="mb-5"/>

          <v-alert
            text
            color="info"
            icon="mdi-github"
          >
            <v-row align="center">
              <v-col class="grow">
                <h3 class="text-h5">
                  Work In Progress
                </h3>
                <div>
                  This application is a <strong>work in progress</strong> and is free
                  and open source which can be found on Github.
                </div>
              </v-col>
              <v-col class="shrink">
                <v-btn icon @click="openGithubDowndown = !openGithubDowndown">
                  <v-icon>mdi-chevron-down</v-icon>
                </v-btn>
              </v-col>
            </v-row>

            <v-expand-transition>
              <div v-show="openGithubDowndown">
                <v-divider
                  class="my-4 info"
                  style="opacity: 0.22"
                ></v-divider>
                <h4>Want to join the development?</h4>
                <p>
                  For anyone in Vanuatu, especially CS students, interested in learning
                  software development, I will be happy to work with you and help you
                  contribute your ideas to this project.
                  <v-btn
                    color="info"
                    outlined
                    @click="openGithub"
                    class="mt-3"
                  >
                    View Source Code
                  </v-btn>
                </p>
                <h4>Have ideas for this application?</h4>
                <p>
                  Find our Facebook page for Bilolok and we can talk about adding your
                  ideas to this project.
                </p>
              </div>
            </v-expand-transition>
          </v-alert>
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <h2>Recent Check-ins</h2>
    </v-container>
    <SectionRecentCheckins />
    <SectionRecentImages />
  </div>
</template>

<script>
import SectionRecentImages from '@/components/home/SectionRecentImages.vue';
import SectionRecentCheckins from '@/components/home/SectionRecentCheckins.vue';

export default {
  name: 'Home',
  components: {
    SectionRecentImages,
    SectionRecentCheckins,
  },
  data() {
    return {
      openGithubDowndown: false,
    };
  },
  methods: {
    openGithub() {
      window.open('https://github.com/michaeltoohig/bilolok');
    },
  },
};
</script>

<style>

</style>

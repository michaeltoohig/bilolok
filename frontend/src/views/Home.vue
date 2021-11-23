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

          <p>
            This application is a <strong>work in progress</strong> and is free and open source
            which can be found on Github.
          </p>

          <v-btn @click="openGithub" class="mb-3">View Github</v-btn>

          <p>
            For anyone in Vanuatu, especially CS students, interested in learning
            software development,
            I will be happy to work with you and help you contribute your ideas to this project.
          </p>
        </v-col>
      </v-row>
    </v-container>
    <SectionRecentCheckins />
    <SectionRecentImages />
  </div>
</template>

<script>
import SectionRecentCheckins from '@/components/home/SectionRecentCheckins.vue';
import SectionRecentImages from '@/components/home/SectionRecentImages.vue';

export default {
  name: 'Home',
  components: {
    SectionRecentCheckins,
    SectionRecentImages,
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

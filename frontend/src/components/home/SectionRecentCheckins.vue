<template>
  <v-container>
    <h2>Recent Checkins</h2>
    <v-row>
      <v-col
        cols="12"
      >
        <v-card
          class="mx-auto"
          color="light"
        >
          <v-list two-line>
            <v-list-item-group>
              <template v-for="item in checkins">
                <v-list-item
                  :key="item.id"
                  :to="{ name: 'Nakamal', params: { id: item.nakamal } }"
                >
                  <template>
                    <v-list-item-content>
                      <v-list-item-title v-text="item.nakamal.id"></v-list-item-title>

                      <v-list-item-subtitle
                        class="text--primary"
                        v-text="item.creatd_at"
                      ></v-list-item-subtitle>

                      <v-list-item-subtitle v-text="item.created_at"></v-list-item-subtitle>
                    </v-list-item-content>
                  </template>
                </v-list-item>
              </template>
            </v-list-item-group>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'SectionRecentCheckins',
  computed: {
    ...mapGetters({
      checkins: 'checkin/recent',
    }),
  },
  beforeMount() {
    this.$store.dispatch('checkin/getRecent');
  },
};
</script>

<style>

</style>

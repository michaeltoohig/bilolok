<template>
  <v-navigation-drawer
    v-model="drawer"
    right
    app
  >
    <v-row
      class="fill-height"
      no-gutters
    >
      <v-navigation-drawer
        app
        right
        dark
        mini-variant
        mini-variant-width="56"
        permanent
      >
        <v-list-item class="px-2">
          <v-list-item-avatar>
            <v-img src="https://randomuser.me/api/portraits/women/75.jpg"></v-img>
          </v-list-item-avatar>
        </v-list-item>

        <v-divider></v-divider>

        <v-list
          dense
          nav
        >
          <v-list-item
            v-for="item in items"
            :key="item.title"
          >
            <v-list-item-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-card
        class="mx-auto my-12"
        max-width="374"
      >
        <template slot="progress">
          <v-progress-linear
            color="deep-purple"
            height="10"
            indeterminate
          ></v-progress-linear>
        </template>

        <v-img
          height="250"
          src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
        ></v-img>

        <v-card-title>Cafe Badilico</v-card-title>

        <v-card-text>
          <v-row
            align="center"
            class="mx-0"
          >
            <v-rating
              :value="4.5"
              color="amber"
              dense
              half-increments
              readonly
              size="14"
            ></v-rating>

            <div class="grey--text ml-4">
              4.5 (413)
            </div>
          </v-row>

          <div class="my-4 subtitle-1">
            $ • Italian, Cafe
          </div>

          <div>Small plates, salads & sandwiches - an intimate setting
            with 12 indoor seats plus patio seating.</div>
        </v-card-text>

        <v-divider class="mx-4"></v-divider>

        <v-card-title>Tonight's availability</v-card-title>

        <v-card-text>
          <v-chip-group
            v-model="selection"
            active-class="deep-purple accent-4 white--text"
            column
          >
            <v-chip>5:30PM</v-chip>

            <v-chip>7:30PM</v-chip>

            <v-chip>8:00PM</v-chip>

            <v-chip>9:00PM</v-chip>
          </v-chip-group>
        </v-card-text>

        <v-card-actions>
          <v-btn
            color="deep-purple lighten-2"
            text
          >
            Reserve
          </v-btn>
        </v-card-actions>
      </v-card>

    </v-row>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'NakamalSideBar',
  data() {
    return {
      items: [
        { title: 'Home', icon: 'mdi-view-dashboard' },
        { title: 'About', icon: 'mdi-forum' },
      ],
      mini: true,
    };
  },
};
</script>

<style>

</style>

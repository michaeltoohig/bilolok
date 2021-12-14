<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Nakamal</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Name</div>
            <div
              class="title primary--text text--darken-2"
              v-if="nakamal"
            >{{nakamal.name}}</div>
            <div
              class="title primary--text text--darken-2"
              v-else
            >-----</div>
          </div>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
          >
            <v-text-field
              label="Name"
              v-model.trim="$v.name.$model"
              :error="$v.name.$error"
              required
            ></v-text-field>
            <v-combobox
              v-model="aliases"
              chips
              clearable
              label="Other Names"
              multiple
            >
              <template v-slot:selection="{ attrs, item, select, selected }">
                <v-chip
                  v-bind="attrs"
                  :input-value="selected"
                  close
                  @click="select"
                  @click:close="removeAlias(item)"
                >
                  <strong>{{ item }}</strong>
                </v-chip>
              </template>
            </v-combobox>
            <v-text-field
              label="owner"
              v-model.trim="$v.owner.$model"
              :error="$v.owner.$error"
              required
            ></v-text-field>
            <v-text-field
              label="Phone"
              v-model.trim="$v.phone.$model"
              :error="$v.phone.$error"
              required
            ></v-text-field>
            <v-text-field
              label="Windows"
              type="number"
              v-model.trim="$v.windows.$model"
              :error="$v.windows.$error"
              required
            ></v-text-field>
            <v-select
              v-model="$v.resources.$model"
              :error="$v.resources.$error"
              :items="allResources"
              item-value="id"
              item-text="name"
              label="Resources"
              multiple
            ></v-select>
            <v-select
              v-model="$v.light.$model"
              :error="$v.light.$error"
              :items="[
                'White',
                'Red',
                'Orange',
                'Yellow',
                'Green',
                'Blue',
                'Purple',
                'Pink',
                'Other',
              ]"
              label="Light Colour"
            ></v-select>
          </v-form>
        </template>
      </v-card-text>
      <v-card-text>
        <v-text-field
          label="Latitude"
          type="text"
          disabled
          required
          :value="$v.lat.$model"
          :error="$v.lat.$error"
        ></v-text-field>
        <v-text-field
          label="Longitude"
          type="text"
          disabled
          required
          :value="$v.lng.$model"
          :error="$v.lng.$error"
        ></v-text-field>

        <div id="map-wrapper">
          <l-map
            style="z-index: 0;"
            ref="map"
            :zoom="zoom"
            :center="center"
            :bounds="bounds"
            :max-bounds="maxBounds"
            :min-zoom="16"
            :max-zoom="18"
            @update:bounds="setBounds"
            @update:center="setCenter"
            @update:zoom="setZoom"
          >
            <l-tile-layer
              :url="url"
              :attribution="attribution"
            />

            <l-marker
              :icon="icon"
              :lat-lng="nakamal.latLng"
            ></l-marker>

            <l-marker
              :icon="icon"
              :lat-lng="center"
            ></l-marker>
          </l-map>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn
          @click="submit"
          :disabled="!valid"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import {
  mapActions,
  mapGetters,
} from 'vuex';
import {
  // integer,
  // minValue,
  validationMixin,
} from 'vuelidate';
import {
  required,
} from 'vuelidate/lib/validators';
import {
  icon, latLngBounds,
} from 'leaflet';
import {
  LMap, LTileLayer, LMarker,
} from 'vue2-leaflet';
import nakamalResourcesApi from '@/api/nakamalResources';

const iconPath = require('../assets/map-marker.svg');

export default {
  name: 'NakamalEdit',
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  mixins: [validationMixin],
  data() {
    return {
      valid: true,
      name: '',
      aliases: [],
      owner: '',
      phone: '',
      light: null,
      windows: 1,
      resources: [],
      allResources: [],
      lat: 0,
      lng: 0,

      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      maxBounds: latLngBounds([
        [-17.627, 168.11],
        [-17.830, 168.47],
      ]),
      icon: icon({
        iconUrl: iconPath,
        iconSize: [54, 44],
        iconAnchor: [16, 40],
      }),
    };
  },
  validations() {
    return {
      name: {
        required,
      },
      aliases: {},
      owner: {},
      phone: {},
      light: {
        required,
      },
      windows: {
        required,
        // integer,
        // minValue: minValue(1),
      },
      resources: {},
      lat: {
        required,
      },
      lng: {
        required,
      },
    };
  },
  computed: {
    ...mapGetters({
      bounds: 'map/bounds',
      center: 'map/center',
      zoom: 'map/zoom',
    }),
    nakamal() {
      return this.$store.getters['nakamal/find'](this.$router.currentRoute.params.id);
    },
  },
  watch: {
    center(newValue) {
      this.lat = newValue.lat;
      this.lng = newValue.lng;
    },
  },
  methods: {
    removeAlias(alias) {
      this.aliases.splice(this.aliases.indexOf(alias), 1);
    },
    reset() {
      this.name = '';
      this.aliases = [];
      this.owner = '';
      this.phone = '';
      this.light = null;
      this.windows = 1;
      this.resources = [];
      this.oldResources = [];
      this.lat = null;
      this.lng = null;

      this.$v.$reset();
      if (this.nakamal) {
        this.name = this.nakamal.name;
        this.aliases = this.nakamal.aliases;
        this.owner = this.nakamal.owner;
        this.phone = this.nakamal.phone;
        this.light = this.nakamal.light;
        this.windows = this.nakamal.windows;
        this.resources = this.nakamal.resources.map((r) => r.id);
        this.oldResources = this.resources; // save original selected resources
        this.lat = this.nakamal.lat;
        this.lng = this.nakamal.lng;
        this.setCenter(this.nakamal.latLng);
      }
    },
    cancel() {
      this.$router.back();
    },
    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) return;

      const payload = {
        name: this.name,
        aliases: this.aliases,
        owner: this.owner,
        phone: this.phone,
        light: this.light,
        windows: this.windows,
        lat: this.lat,
        lng: this.lng,
      };
      this.$store.dispatch('nakamal/update', { nakamalId: this.nakamal.id, payload });
      this.$store.dispatch('nakamal/updateResources', {
        nakamalId: this.nakamal.id,
        oldResources: this.oldResources,
        resources: this.resources,
      });
      this.$router.push({ name: 'Nakamal', id: this.nakamal.id });
    },
    ...mapActions(
      'map', [
        'setBounds',
        'setCenter',
        'setZoom',
      ],
    ),
  },
  async mounted() {
    await this.$store.dispatch('nakamal/load');
    const response = await nakamalResourcesApi.getAll();
    this.allResources = response.data;
    this.setCenter(this.nakamal.latLng);
    this.reset();
  },
};
</script>

<style scoped>
#map-wrapper {
  height: 300px;
}
</style>

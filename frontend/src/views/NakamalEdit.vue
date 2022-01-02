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
            >{{ nakamal.name }}</div>
            <div
              class="title primary--text text--darken-2"
              v-else
            >-----</div>
          </div>
          <v-form
            ref="form"
          >
            <v-text-field
              label="Name"
              v-model.trim="$v.name.$model"
              :error="$v.name.$error"
              required
            ></v-text-field>
            <v-combobox
              v-model="$v.aliases.$model"
              :error="$v.aliases.$error"
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
            <SelectLight
              v-model="$v.light.$model"
              :error="$v.light.$error"
            ></SelectLight>
            <SelectKavaSource
              v-model="$v.kava_source.$model"
              :error="$v.kava_source.$error"
            ></SelectKavaSource>
          </v-form>
        </template>
      </v-card-text>
      <v-card-text>
        <div class="mb-5">
          <SelectArea
            v-model="$v.area.$model"
            :error="$v.area.$error"
          ></SelectArea>
        </div>

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

        <v-btn
          text
          outlined
          @click="toggleMap"
          class="mb-3"
        >
          Update location
        </v-btn>
        <v-expand-transition>
          <div v-show="showMap">
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
            <v-btn
              outlined
              @click="setNewLocation"
              class="mt-3"
            >Set New Location</v-btn>
          </div>
        </v-expand-transition>
      </v-card-text>
      <v-card-actions>
        <v-btn
          @click="submit"
          text
          outlined
          color="primary"
        >
          Save
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn text @click="cancel">Cancel</v-btn>
        <v-btn text @click="reset">Reset</v-btn>
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
  validationMixin,
} from 'vuelidate';
import {
  required,
  minValue,
} from 'vuelidate/lib/validators';
import {
  icon, latLngBounds,
} from 'leaflet';
import {
  LMap, LTileLayer, LMarker,
} from 'vue2-leaflet';
import nakamalResourcesApi from '@/api/nakamalResources';
import SelectArea from '@/components/SelectArea.vue';
import SelectKavaSource from '@/components/SelectKavaSource.vue';
import SelectLight from '@/components/SelectLight.vue';

const iconPath = require('../assets/map-marker.svg');

export default {
  name: 'NakamalEdit',
  components: {
    SelectArea,
    SelectKavaSource,
    SelectLight,
    LMap,
    LTileLayer,
    LMarker,
  },
  mixins: [validationMixin],
  data() {
    return {
      name: '',
      aliases: [],
      owner: '',
      phone: '',
      light: null,
      windows: 1,
      resources: [],
      allResources: [],
      area: null,
      kava_source: null,
      lat: 0,
      lng: 0,
      // currentNakamalLocation: null,

      showMap: false,
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
        minValue: minValue(1),
      },
      resources: {},
      area: {
        required,
      },
      kava_source: {
        required,
      },
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
  methods: {
    toggleMap() {
      this.showMap = !this.showMap;
      setTimeout(() => {
        this.$refs.map.mapObject.invalidateSize();
      }, 250);
    },
    setNewLocation() {
      const { lat, lng } = this.center;
      this.lat = lat;
      this.lng = lng;
      this.$store.dispatch('notify/add', {
        type: 'info',
        title: 'Location Updated',
        text: 'The new nakamal location will be saved.',
        duration: 3_000,
      });
    },
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
      this.area = null;
      this.kava_source = null;
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
        this.area = this.nakamal.area.id;
        this.kava_source = this.nakamal.kava_source.id;
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
        area_id: this.area,
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
    async getResources() {
      const response = await nakamalResourcesApi.getAll();
      this.allResources = response.data;
    },
  },
  async mounted() {
    await this.$store.dispatch('nakamal/load');
    this.getResources();
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

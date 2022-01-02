<template>
  <v-dialog
    v-model="dialog"
    persistent
    max-width="600px"
  >
    <template v-slot:activator="{ on, attrs }">
      <l-marker
        v-if="show"
        :lat-lng="center"
        :icon="icon"
      >
        <l-tooltip :options="{
          permanent: true,
          interactive: true,
          direction: 'top',
          offset: [0, -40]
        }">
          <v-btn
            x-small
            text
            color="black"
            v-bind="attrs"
            v-on="on"
          >
            Add New Kava Bar
          </v-btn>
        </l-tooltip>
      </l-marker>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">Kava Bar</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                v-model="$v.name.$model"
                :error="$v.name.$error"
                label="Name"
                required
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <SelectLight
                v-model="$v.light.$model"
                :error="$v.light.$error"
              ></SelectLight>
            </v-col>
            <v-col
              cols="12"
            >
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
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <SelectArea
                v-model="$v.area.$model"
                :error="$v.area.$error"
              ></SelectArea>
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                v-model="$v.windows.$model"
                :error="$v.windows.$error"
                label="# of Windows"
                type="number"
                required
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <SelectKavaSource
                v-model="$v.kava_source.$model"
                :error="$v.kava_source.$error"
              ></SelectKavaSource>
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <v-select
                v-model="$v.resources.$model"
                :error="$v.resources.$error"
                :items="allResources"
                item-value="id"
                item-text="name"
                label="Resources"
                multiple
              ></v-select>
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                v-model="$v.owner.$model"
                :error="$v.owner.$error"
                label="Owner"
                type="text"
                required
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                v-model="$v.phone.$model"
                :error="$v.phone.$error"
                label="Contact Number"
                type="text"
                required
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                label="Latitude"
                type="text"
                disabled
                required
                :value="center.lat"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                label="Longitude"
                type="text"
                disabled
                required
                :value="center.lng"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-btn
          color="primary"
          outlined
          text
          @click="submit"
        >
          Submit
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          text
          @click="dialog = false"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  mapGetters,
} from 'vuex';
import {
  LMarker,
  LTooltip,
} from 'vue2-leaflet';
import {
  validationMixin,
} from 'vuelidate';
import {
  required,
  minValue,
} from 'vuelidate/lib/validators';
import {
  icon,
} from 'leaflet';
import nakamalResourcesApi from '@/api/nakamalResources';
import SelectArea from '@/components/SelectArea.vue';
import SelectKavaSource from '@/components/SelectKavaSource.vue';
import SelectLight from '@/components/SelectLight.vue';

const iconPath = require('../assets/map-marker.svg');

export default {
  name: 'NewNakamalDialog',
  components: {
    SelectArea,
    SelectKavaSource,
    SelectLight,
    LMarker,
    LTooltip,
  },
  mixins: [validationMixin],
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      dialog: false,
      icon: icon({
        iconUrl: iconPath,
        iconSize: [54, 44],
        iconAnchor: [16, 40],
      }),
      openAddArea: false,

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
    };
  },
  computed: {
    ...mapGetters({
      center: 'map/center',
    }),
    form() {
      return {
        name: this.name,
        aliases: this.aliases,
        windows: this.windows,
        owner: this.owner,
        phone: this.phone,
        lat: this.center.lat,
        lng: this.center.lng,
        light: this.light,
        resources: this.resources,
        area_id: this.area,
        kava_source_id: this.kava_source,
      };
    },
  },
  methods: {
    changeArea(area) {
      console.log('xxy', area);
    },
    async getResources() {
      const response = await nakamalResourcesApi.getAll();
      this.allResources = response.data;
    },
    removeAlias(alias) {
      this.aliases.splice(this.aliases.indexOf(alias), 1);
    },
    async submit() {
      this.$v.$touch();
      if (this.$v.$invalid) return;

      await this.$store.dispatch('nakamal/add', this.form);
      this.$store.dispatch('map/setShowNewNakamalMarker', false);
      this.dialog = false;
    },
  },
  async mounted() {
    this.getResources();
  },
};
</script>

<style>

</style>

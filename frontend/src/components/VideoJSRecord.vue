<template>
  <div>
    <video id="myVideo" playsinline class="video-js vjs-default-skin">
      <p class="vjs-no-js">
        To view this video please enable JavaScript, or consider upgrading to a
        web browser that
        <a href="https://videojs.com/html5-video-support/" target="_blank">
          supports HTML5 video.
        </a>
      </p>
    </video>
    <div id="myControls" class="my-3 d-flex flex-row justify-center">
      <div v-if="isSaveDisabled">
        <v-btn
          icon
          :disabled="!hasMultipleDevices || isStartRecording"
          @click.prevent="nextDevice"
        >
          <v-icon>mdi-camera-flip</v-icon>
        </v-btn>
        <v-btn
          v-if="!isStartRecording"
          icon
          color="red"
          :disabled="!isDeviceReady"
          @click.prevent="startRecording"
        >
          <v-icon>mdi-record</v-icon>
        </v-btn>
        <v-btn
          v-else
          icon
          @click.prevent="stopRecording"
        >
          <v-icon>mdi-stop</v-icon>
        </v-btn>
      </div>
      <div v-else>
        <v-btn
          icon
          @click.prevent="submitVideo"
        >
          <v-icon>mdi-upload</v-icon>
        </v-btn>
        <v-btn
          icon
          @click.prevent="retakeVideo"
        >
          <v-icon>mdi-restore</v-icon>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import 'video.js/dist/video-js.css';
import 'videojs-record/dist/css/videojs.record.css';
import videojs from 'video.js';

import 'webrtc-adapter';
import RecordRTC from 'recordrtc';

import Record from 'videojs-record/dist/videojs.record.js';
// import FFmpegjsEngine from 'videojs-record/dist/plugins/videojs.record.ffmpegjs.js';

export default {
  name: 'VideoJSRecord',
  props: ['enable'],
  emits: ['recorded-data'],
  data() {
    return {
      devices: null,
      selectedDevice: null,

      player: null,
      retake: 0,
      isDeviceReady: false,
      isSaveDisabled: true,
      isStartRecording: false,
      // isRetakeDisabled: true,
      // submitText: 'Submit',
      options: {
        fluid: true,
        // fill: true,
        // responsive: true,
        width: '100%',
        height: '100%',
        controls: true,
        bigPlayButton: false,
        controlBar: {
          volumePanel: false,
          deviceButton: false,
          recordToggle: false,
          fullscreenToggle: false,
          pipToggle: false,
        },
        // fluid: true,
        plugins: {
          record: {
            debug: true,
            autoMuteDevice: true,
            pip: false,
            audio: true,
            maxLength: 10,
            aspectRatio: '1:1',
            video: {
              width: {
                min: 480,
                ideal: 480,
                max: 1280,
              },
              height: {
                min: 480,
                ideal: 480,
                max: 1280
              }
            },
            frameWidth: 480,
            frameHeight: 480,
          },
        },
      },
    };
  },
  computed: {
    hasMultipleDevices() {
      return this.devices !== null && this.devices.length > 1
    },
  },
  watch: {
    enable(val) {
      // Stop recording
      if (this.player) {
        if (val) {
          this.player.reset();
          this.initPlayer()
        } else {
          this.player.record().stopDevice();
        }
      }
    },
  },
  mounted() {
    this.player = videojs('myVideo', this.options, () => {
      // print version information at startup
      const msg = `Using video.js ${videojs.VERSION} with videojs-record ${videojs.getPluginVersion('record')} and recordrtc ${RecordRTC.version}`;
      videojs.log(msg);
    });
    this.initPlayer();
    // error handling
    this.player.on('deviceReady', () => {
      console.log('device ready:');
      this.isDeviceReady = true;
    });
    this.player.on('deviceError', () => {
      console.log('device error:', this.player.deviceErrorCode);
    });
    this.player.on('error', (element, error) => {
      console.error(error);
    });
    // user clicked the record button and started recording
    this.player.on('startRecord', () => {
      console.log('started recording!');
    });
    // user completed recording and stream is available
    this.player.on('finishRecord', () => {
      this.isStartRecording = false;
      this.isSaveDisabled = false;
      // if (this.retake === 0) {
      //     this.isRetakeDisabled = false;
      // }
      // the blob object contains the recorded data that
      // can be downloaded by the user, stored on server etc.
      console.log('finished recording: ', this.player.recordedData);
    });
    // enumerate multiple video input devices
    this.player.on('enumerateReady', () => {
      const devices = this.player.record().devices;
      this.devices = devices.filter((d) => d.kind === 'videoinput').map((d) => d.deviceId);
    });
  },
  methods: {
    initPlayer() {
      this.isDeviceReady = false;
      this.isSaveDisabled = true;
      this.isStartRecording = false;
      // enumerate devices once
      this.player.record().enumerateDevices();
      // start playing the initial device
      this.player.record().getDevice();
    },
    nextDevice() {
      if (this.devices.length <= 1) return;
      this.isDeviceReady = false;
      if (this.selectedDevice === null) {
        this.selectedDevice = 1;
      } else {
        if (this.devices.length > this.selectedDevice) {
          this.selectedDevice += 1;
        } else {
          this.selectedDevice = 0;
        }
      }
      this.player.record().setVideoInput(this.devices[this.selectedDevice]);
      this.player.record().getDevice();
    },
    startRecording() {
      this.isStartRecording = true;
      this.player.record().start();
    },
    stopRecording() {
      this.isStartRecording = false;
      this.player.record().stop();
    },
    submitVideo() {
      this.isSaveDisabled = true;
      // this.isRetakeDisabled = true;
      const data = this.player.recordedData;
      this.player.record().stopDevice();
      this.$emit('recorded-data', data);
    },
    retakeVideo() {
      this.isSaveDisabled = true;
      this.player.record().getDevice();
      // this.isRetakeDisabled = true;
      // this.retake += 1;
    },
  },
  beforeDestroy() {
    if (this.player) {
      this.player.record().destroy();
      this.player.dispose();
    }
  },
};
</script>

<style scoped>

</style>

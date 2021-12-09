import dayjs from 'dayjs';

export default {
  computed: {
    timelineItems() {
      const newList = this.images.concat(this.checkins);
      return newList.sort((a, b) => (dayjs(b.created_at).isAfter(a.created_at) ? 1 : -1));
    },
  },
  methods: {
    getItemType(item) {
      // TODO Hacky way to find object type - should be improved
      if ('private' in item) return 'checkin';
      if ('src' in item) return 'image';
      return 'other';
    },
  },
};

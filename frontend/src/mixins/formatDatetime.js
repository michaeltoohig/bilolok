import dayjs from 'dayjs';
import RelativeTime from 'dayjs/plugin/relativeTime';
import LocalizedFormat from 'dayjs/plugin/localizedFormat';

dayjs.extend(RelativeTime);
dayjs.extend(LocalizedFormat);

export default {
  methods: {
    formatTimeAgo(d) {
      return dayjs(d).fromNow();
    },
    formatTime(d) {
      return dayjs(d).format('LLL');
    },
  },
};

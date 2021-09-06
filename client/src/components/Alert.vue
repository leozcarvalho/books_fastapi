<template>
<div>
  <b-alert
    :variant = "variant"
    :show="dismissCountDown"
    dismissible
    @dismissed="dismissCountDown=0"
    @dismiss-count-down="countDownChanged"
    >{{ message }}
  </b-alert>
</div>
</template>

<script>
export default {
  data() {
    return {
      message: '',
      showMessage: false,
      dismissCountDown: 0,
      variant: '',
    };
  },
  methods: {
    showAlert(message, variant) {
      this.dismissCountDown = 5;
      this.variant = variant;
      this.message = message;
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
  },
};
</script>

<template>
  <div></div>
</template>

<script>
export default {
  mounted () {
    for (let key in this.$listeners) {
      window.addEventListener(key, this.$listeners[key])
    }
  },
  beforeDestroy () {
    for (let key in this.$listeners) {
      window.removeEventListener(key, this.$listeners[key])
    }
  }
}
</script>

<style>

</style>

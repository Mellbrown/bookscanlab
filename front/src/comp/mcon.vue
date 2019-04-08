<template>
  <div class="flex h-left mx-1">
    <div tabindex="0"
      class="grow bg-dark mx-1 p-1 rounded"
      v-for="(val, key) in value" :key="key">

      <small class="px-1">{{ key }}</small>
      <input class="w-100 h-50 rounded" v-model="value[key]">
    </div>
  </div>
</template>

<script>
export default {
  props: [ 'value', 'init', 'name' ],
  mounted () {    
    this.$emit('input', { ...this.init })
  },
  watch: {
    name () {
      var self = this
      this.$nextTick(() => {
        self.$emit('input', { ...self.init })
      })
    }
  }
}
</script>

<style>

</style>

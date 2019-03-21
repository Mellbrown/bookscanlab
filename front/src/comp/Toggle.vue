<template>
  <div class="toggle bg-primary" @click="$emit('click')">
    <small class="mr-1">{{label}}</small>
    <icon icon="toggle-on" size="lg" v-if="on"/>
    <icon icon="toggle-off" size="lg" v-else/>
  </div>
</template>

<script>
export default {
  props: ['on', 'label']
}
</script>

<style lang="scss" scoped>
.toggle {
  padding: 0pt 10pt;
  border-radius: 9pt;
  cursor: pointer;
}
</style>

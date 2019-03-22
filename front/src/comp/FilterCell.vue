<template>
  <div class="cell" tabindex="0">
  <div class="flex h-left">
    <h6>{{title}}</h6>
    <div class="flex h-right grow">
      <toggle :label="visible ? 'visible' : 'invisible'" :on="visible" @click="$emit('toggle-visible')"/>
    </div>
  </div>
  <small>{{description}}</small>
  <div class="flex h-right px-2 py-1">
    <div class="flex">
      <small class="block bg-secondary rounded px-2 mb-1"  v-for="(val, key) in property" :key="key">{{key}}: {{val}}</small>
    </div>
  </div>
</div>
</template>

<script>
import Toggle from '@/comp/Toggle'

export default {
  props: {
    title: { type: String, required: true },
    description: { type: String, default: '' },
    visible: { type: Boolean, default: false },
    property: { type: Object, default: (() => {})() }
  },
  components: { Toggle }
}
</script>

<style lang="scss" scoped>
@import "bootstrap/scss/bootstrap.scss";

.cell {
  @extend .card, .pt-1, .mb-2, .p-2, .bg-info ;
  cursor: pointer;
}
</style>

<template>
  <div class="frame relative">
    <div :style="st" v-for="(st, i) in divStyle" :key="i"
      class="bg-warning in-block absolute">
    </div>
  </div>
</template>

<script>
export default {
  props: {
    scale: { type: Number, required: true },
    coord: { type: Object, required: true },
    width: { type: Number, required: true },
    height: { type: Number, required: true },
    depths: { type: Array, required: true },
    translate: { type: Object }
  },
  computed: {
    scoord () { return { x: this.scale * this.coord.x, y: this.scale * this.coord.y } },
    swdith () { return this.scale * this.width },
    sheight () { return this.scale * this.height },
    divStyle () {
      var cnt = this.depths.length
      var w = this.width / cnt
      var result = []
      for (var i = 0; cnt - 1 > i; i++) {
        result.push({
          width: w + 'px',
          height: this.height + 'px',
          transformOrigin: 'top left',
          transform: `translate3d(${
            this.scoord.x + this.swdith * i / cnt
            }, ${this.scoord.y}) scale(${this.scale})`,
          opacity: '0.5'
        })
      }
      return result
    }
  }
}
</script>

<style>

</style>

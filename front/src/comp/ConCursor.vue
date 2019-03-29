<template>
  <div tabindex="0" class="rounded bg-dark flex h-left"
    @keydown="keydown">
    <div class="flex grow p-2" v-for="i in 2" :key="i">
      <small class="text-light">{{name[i - 1]}} :</small>
      <input v-if="i === 1"  @keydown="keydown"
        class="w-100 rounded border mt-1" tabindex="-1"
        v-model.number="val1"/>
      <input v-else @keydown="keydown"
        class="w-100 rounded border mt-1" tabindex="-1"
        v-model.number="val2"/>
    </div>
  </div>
</template>

<script>
export default {
  props: ['name', 'init', 'step'],
  data () {
    return {
      val1: 0,
      val2: 0
    }
  },
  mounted () {
    this.val1 = this.init[0]
    this.val2 = this.init[1]
  },
  watch: {
    val1 () {
      this.$emit('changed', [this.val1, this.val2])
    },
    val2 () {
      this.$emit('changed', [this.val1, this.val2])
    }
  },
  methods: {
    keydown (e) {
      switch (e.key) {
        case 'ArrowUp':
          this.val1 += this.step[0]
          break
        case 'ArrowDown':
          this.val1 -= this.step[0]
          break
        case 'ArrowLeft':
          this.val2 -= this.step[1]
          break
        case 'ArrowRight':
          this.val2 += this.step[1]
          break
      }
    }
  }
}
</script>

<style>

</style>

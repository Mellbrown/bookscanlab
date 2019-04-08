<template>
  <div class="bg-secondary text-light mt-2 mx-3 rounded px-3 py-2">
    <div class="flex h-left between">
      <h5>{{ title }}</h5>
      <button class="btn btn-primary btn-sm" @click="add">
        <icon icon="plus"/>
      </button>
    </div>
    <div v-for="(f, i) in value" :key="i" class="flex h-left my-1 between">
      <select class="form-control w-25" v-model="f.name">
        <option>box</option>
        <option>bilateral</option>
        <option>median</option>
        <option>blur</option>
        <option>gaussian</option>
      </select>
      <mcon
        class="flex h-left grow"
        :value="f.param"
        @input="f.param = $event"
        :name="f.name"
        :init="
          f.name === 'box' ? { ksize: 11 } :
          f.name === 'bilateral' ? { d: 1, sColor: 10, sSpace: 10 } :
          f.name === 'median' ? { ksize: 7 } :
          f.name === 'blur' ? { ksize: 7 } :
          f.name === 'gaussian' ? { ksize: 7, sigmaX: 0 } : {}"/>
      <button class="btn btn-danger btn-sm" @click="lstDel(i)">
        <icon icon="trash-alt" />
      </button>
    </div>
  </div>
</template>

<script>
import mcon from '@/comp/mcon'

export default {
  props: ['value', 'title'],
  methods: {
    add () {
      this.$emit('input', this.value.concat({ name: null, param: null }))
    },
    lstDel (idx) {
      this.$emit('input', this.value.filter((item, i) => idx !== i))
    }
  },
  components: { mcon }
}
</script>

<style>

</style>

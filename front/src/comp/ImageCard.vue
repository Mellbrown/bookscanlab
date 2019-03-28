<template>
  <div class="card m-1 point" @click="selectSource(src)">
    <img class="card-img-top" :src="src_url"/>
    <div class="card-body bg-secondary p-2 text-light">
      <small class="card-text">{{src}}</small>
    </div>
  </div>
</template>

<script>
import { mapMutations, mapState } from 'vuex'
export default {
  props: ['src'],
  methods: {
    ...mapMutations([
      'selectSource'
    ])
  },
  computed: {
    src_url () {
      return this.rHost + '/static/source/' + this.src
    },
    ...mapState(['rHost'])
  }
}
</script>

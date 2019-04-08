<template>
  <div class="bg-warning flex h-100 y-scroll">
    <window-event @keyup.r="runFilter" />
    <h3 class="m-cell mt-3">필터 설정</h3>
    <div class="m-cell">
      <h5>src</h5>
      <div>
        height: {{ }}, width: {{ }}
      </div>
    </div>

    <cmd-filter v-model="prevFilter" title="prev filter"/>

    <div class="m-cell">
      <h5>gray</h5>
    </div>

    <cmd-filter v-model="afterFilter" title="after filter"/>

    <div class="v-cell">
      <h5>cany</h5>
      <con-cursor
        @changed="canyA = $event[0]; canyB = $event[1]"
        :name="['cany A','cany B']" :init="[30, 230]" :step="[10,10]"/>
    </div>

    <div class="v-cell">
      <div class="flex h-left between centerline">
        <h5>dilate</h5>
        <input type="checkbox" class="mr-3" v-model="dilateOn">
      </div>
      <con-cursor
        @changed="kernel = $event[0]; it = $event[1]"
        :name="['kernel','it']" :init="[3, 1]" :step="[1,1]"/>
    </div>
    
    <div class="m-cell">
      <h5>Contours</h5>
    </div>

    <div class="v-cell">
      <h5>poly</h5>
      <con-cursor
        @changed="polydp = $event[0];"
        :name="['polydp','-']" :init="[1, 0]" :step="[1, 0]"/>
    </div>

    <div style="height: 300px; width: 100%;">

    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ConCursor from '@/comp/ConCursor'
import cmdFilter from '@/comp/cmdFilter'
import axios from 'axios'

export default {
  data () {
    return {
      canyA: 0,
      canyB: 0,
      kernel: 0,
      it: 0,
      dilateOn: false,
      polydp: 0,
      prevFilter: [],
      afterFilter:[]
    }
  },
  methods:{
    runFilter () {
      var self = this
      var dpost = {
        image: this.selectedSource,
        'filter-param': {
          'prev-filter': this.prevFilter,
          'after-filter': this.afterFilter,
          'cany-0': this.canyA,
          'cany-1': this.canyB,
          dilate: {
            on: this.dilateOn,
            kernel: this.kernel,
            it: this.it
          },
          polydp: this.polydp
        }
      }
      console.log(dpost)

      axios.post(this.rHost + '/run-filter', dpost)
      .then(body => {
        self.$emit('loaded', body.data[0])
      })
    }
  },
  computed: {
    ...mapState([
      'selectedSource',
      'rHost'
    ]),
  },
  components: { ConCursor, cmdFilter }
}
</script>

<style lang="scss" scoped>
@import "~bootstrap/scss/bootstrap";
@import "../util";

.m-cell {
  @extend
    .flex,
    .between,
    .h-left,
    .mx-3,
    .mt-2,
    .text-light,
    .rounded,
    .bg-secondary,
    .px-3,
    .py-2 ;
  align-items: center;
}

.v-cell {
    @extend
    .flex,
    .between,
    .mx-3,
    .mt-2,
    .text-light,
    .rounded,
    .bg-secondary,
    .px-3,
    .py-2 ;
}
</style>

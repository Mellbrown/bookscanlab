<template>
  <div class="container-fliud flex grow h-left">
    <div class="col-md-6 bg-secondary flex grow p-0">
      <image-viewer :src="selectedSource" @points-changed="pointsChanged" :pointover="pointover" v-if="selectedSource"/>
    </div>
    <div class="col-md-3 flex grow  bg-secondary">
      <h3 class="mt-1 bg-primary p-1 px-2 text-light rounded">poly points</h3>
      <div class="flex grow card m-1 p-1 y-scroll">
        <div
          class="m-1 p-1 px-2 bg-secondary rounded flex h-left text-light clpoint"
          v-for="(p,i) in childPoints" :key="i"
          @mouseenter="pointover=i"
          @mouseleave="pointover=-1">
          <div class="mr-2">{{i}} | </div>
          <div class="grow mr-1">x: {{p.x}}</div>
          <div class="grow">y: {{p.y}}</div>
        </div>
      </div>
      <div class="flex grow relative my-3 mx-1">
        <textarea class="frame card" v-model="jsonPoint"></textarea>
      </div>
    </div>
    <div class="col-md-3 bg-secondary">
      <h3 class="mt-1 bg-primary p-1 px-2 text-light rounded">3D Paper</h3>
    </div>
  </div>
</template>

<script>
import ImageViewer from '@/comp/ImageViewer'
import { mapState } from 'vuex'
export default {
  data () {
    return {
      childPoints: [],
      pointover: -1,
      jsonPoint: ''
    }
  },
  computed: {
    ...mapState([
      'selectedSource'
    ])
  },
  methods: {
    pointsChanged (points) {
      this.childPoints = points
    }
  },
  watch: {
    childPoints () {
      this.jsonPoint = JSON.stringify(this.childPoints)
    }
  },
  components: { ImageViewer }
}
</script>

<style lang="scss" scoped>
@import "~bootstrap/scss/bootstrap";

.clpoint:hover{
  @extend .bg-primary;
}

</style>

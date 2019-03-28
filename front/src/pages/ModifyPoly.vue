<template>
  <div class="container-fliud flex grow h-left">
    <div class="col-lg-6 col-sm-12 bg-secondary flex grow p-0">
      <image-viewer v-if="selectedSource"
        @points-changed="pointsChanged"
        @source-size="srcheight = $event[0]; srcwidth = $event[1]"
        :src="src_url"
        :pointover="pointover"
        :visible3dpaper="visible3dpaper"
        :page3d="page3d"/>
    </div>
    <div class="col-md-3 visible-md flex grow  bg-secondary">
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
    <div class="col-md-3 visible-md bg-secondary">
      <h3 class="mt-1 bg-primary p-1 px-2 text-light rounded">3D Paper</h3>
      <div class="bg-dark p-1 px-3 mb-1 rounded text-light flex h-left">
        <div>3d pager visibility: </div>
        <div class="grow text-right"><input type="checkbox" class="form-check-inpu" v-model="visible3dpaper"></div>
      </div>
      <div class="bg-dark rounded text-light p-1 flex" style="height: 200px">
        <div class="flex h-right mb-1">
          <button class="btn btn-primary btn-sm ml-1"
            @click="page3d.depth.push(1)"><icon icon="plus"/></button>
          <button class="btn btn-primary btn-sm"
            @click="page3d.depth.pop()"><icon icon="minus"/></button>
          <div class="relative mr-3"><div class="midcen">{{page3d.depth.length}}</div></div>
          <div class="grow ml-2">curvature</div>
        </div>
        <div class="grow bg-secondary rounded m-1 relative">
          <div class="frame">
            <div  class="lcen-to border border-warning w-100" style="left:0px; top:50%"></div>
            <small class="lcen-to" style="left:0px; top:50%">1</small>
            <small class="lcen-to" style="left:0px; top:5%">2</small>
            <small class="lcen-to" style="left:0px; top:95%">0</small>
          </div>
        </div>
      </div>
      <con-cursor class="my-1"
        @changed="page3d.height = $event[0]; page3d.width = $event[1]"
        :name="['page height','pager width']" :init="[2160,1490]" :step="[10,10]"/>
      <con-cursor class="my-1"
        @changed="page3d.y = $event[0]; page3d.x = $event[1]"
        :name="['page y','pager x']" :init="[140,260]" :step="[10,10]"/>
      <con-cursor class="my-1"
        @changed="page3d.cameray = $event[0]; page3d.camerax = $event[1]" v-if="srcheight"
        :name="['camera y','camera x']" :init="[srcheight/2,srcwidth/2]" :step="[10,10]"/>
    </div>
  </div>
</template>

<script>
import ImageViewer from '@/comp/ImageViewer'
import ConCursor from '@/comp/ConCursor'
import { mapState } from 'vuex'

export default {
  data () {
    return {
      srcheight: null,
      srcwidth: null,
      childPoints: [],
      pointover: -1,
      jsonPoint: '',
      visible3dpaper: false,
      page3d: {
        camerax: 300,
        cameray: 500,
        cameraz: 0.1,
        x: 100,
        y: 100,
        height: 1000,
        width: 600,
        depth: [2, 2, 2, 2, 2, 2, 1.965, 1.955, 1.95, 1.95, 1.96, 2]
      }
    }
  },
  computed: {
    ...mapState([
      'selectedSource', 'rHost'
    ]),
    src_url () {
      return this.rHost + '/static/source/' + this.selectedSource
    }
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
  components: { ImageViewer, ConCursor }
}
</script>

<style lang="scss" scoped>
@import "~bootstrap/scss/bootstrap";

.clpoint:hover{
  @extend .bg-primary;
}

</style>

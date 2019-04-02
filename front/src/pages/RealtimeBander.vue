<template>
  <div class="flex grow container-fluid p-0 h-left">
    <div class="col-lg-2 col-md-2 bg-warning flex p-3">
      <button class="btn btn-lg"
        :class="[ polyWatching ? 'btn-success' : 'btn-secondary']"
        @click="polyWatching = !polyWatching; transferPoly()">
        Watch
      </button>
      <con-cursor class="my-1"
        @changed="resultBound.top = $event[0]; resultBound.left = $event[1]"
        :name="['bound top','bound left']" :init="[100,100]" :step="[10,10]"/>
      <con-cursor class="my-1"
        @changed="resultBound.height = $event[0]; resultBound.width = $event[1]"
        :name="['result height','result width']" :init="[2000,1400]" :step="[10,10]"/>
    </div>
    <image-viewer v-if="src_url"
      class="col-md-5 p-0 bg-secondary"
      @points-changed="points = $event"
      @source-size="srcheight = $event[0]; srcwidth = $event[1]"
      :src="src_url"
      :pointover="pointover"
      :visible3dpaper="false"
      :page3d="{}"/>
    <image-viewer-lite :images="resultImages" />
  </div>
</template>

<script>
import ImageViewer from '@/comp/ImageViewer'
import ImageViewerLite from '@/comp/ImageViewerLite'
import ConCursor from '@/comp/ConCursor'
import { mapState } from 'vuex'
import axios from 'axios'

export default {
  data () {
    return {
      resultBound: {
        height: 0,
        width: 0,
        left: 0,
        top: 0
      },
      srcheight: null,
      srcwidth: null,
      pointover: -1,
      points: null,
      polyWatching: false,
      resultImages: []
    }
  },
  methods: {
    transferPoly () {
      axios.post(`${this.rHost}/image-banding`, {
        coord: this.points,
        image: this.selectedSource,
        bound: this.resultBound
      })
        .then(response => {
          this.resultImages = response.data
        })
    }
  },
  computed: {
    ...mapState([
      'selectedSource',
      'rHost'
    ]),
    src_url () {
      return this.rHost + '/static/source/' + this.selectedSource
    },
    resultImagesURLS () {
      return this.resultImages.map(img => this.rHost + '/static/' + img)
    }
  },
  watch: {
    points () {
      if (this.polyWatching) {
        this.transferPoly()
      }
    }
  },
  components: { ImageViewer, ConCursor, ImageViewerLite }
}
</script>

<style>

</style>

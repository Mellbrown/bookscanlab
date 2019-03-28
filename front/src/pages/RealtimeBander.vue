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
    <div class="flex">
      <img class="img-fluid" :src="rHost + '/static/' + resultImages[0]" v-if="resultImages[0]"/>
    </div>
  </div>
</template>

<script>
import ImageViewer from '@/comp/ImageViewer'
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
      txtRequest: '',
      resultImages: []
    }
  },
  methods: {
    transferPoly () {
      axios.post(`${this.rHost}/image-banding`, {
        path: this.points,
        'image-target': this.selectedSource,
        bound: this.resultBound
      })
        .then(response => {
          console.log(response)
          this.resultImages = response.data
          this.txtRequest = 'success: ' + response.data
        })
        .catch(error => {
          console.log(error)
          this.txtRequest = 'error: ' + error.data
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
    }
  },
  watch: {
    points () {
      if (this.polyWatching) {
        this.transferPoly()
      }
    }
  },
  components: { ImageViewer, ConCursor }
}
</script>

<style>

</style>

<template>
  <div class="flex grow">
    <window-event v-if="drag"
      @mousemove="
        drag.diffX = $event.clientX - drag.orgX
        drag.diffY = $event.clientY - drag.orgY"
      @mouseup="
        shown.left += drag.diffX
        shown.top += drag.diffY
        drag = null"/>

    <div class="flex">
      <div class="p-1 px-3 bg-dark flex">
        <div class="mx-auto">
          <button class="btn btn-primary mx-1" @click="rotate -= 90">
            <icon icon="undo-alt"/>
          </button>
          <button class="btn btn-primary mx-1" @click="rotate += 90">
            <icon icon="redo-alt"/>
          </button>
        </div>
      </div>
    </div>
    <div
      ref="con"
      class="flex grow relative"
      style="overflow: hidden;"
      @mousewheel="shown.width -= $event.deltaY * 1.5"
      @mousedown="drag = { orgX: $event.clientX, orgY: $event.clientY, diffX: 0, diffY: 0 }">
      <div class="absolute in-block shadow" v-if="selected"
        :style="{
          width: `${shown.width}px`,
          height: `${shown.height}px`,
          transform: `
            translate(
              ${shown.left + (drag ? drag.diffX : 0) }px,
              ${shown.top + (drag ? drag.diffY : 0) }px
            )
            rotate(${shown.rotate}deg)
          `.replace('\n', '')
        }">
        <img :src="rHost + '/static/' + selected" class="frame" ref="img" draggable="false"/>
      </div>
    </div>
    <div class="bg-dark" style="overflow-x: scroll;">
      <img
        @click="selected = img"
        :src="rHost + '/static/' + img"
        v-for="(img, i) in images" :key="i"
        style="height: 80px; width: 60px;"
        />
      </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    images: { type: Array, default: () => [] }
  },
  data () {
    return {
      selected: null,
      origin: {
        height: 0,
        width: 0,
        ratio: 1
      },
      shown: {
        left: 0,
        top: 0,
        width: 600,
        height: 600,
        scale: 1,
        rotate: 0
      },
      drag: null
    }
  },
  mounted () {

  },
  computed: {
    ...mapState(['rHost'])
  },
  watch: {
    images () {
      if (this.images.length > 0) {
        this.selected = this.images[0]
      }
    },
    selected () {
      var self = this
      this.$nextTick(() => {
        self.origin = {
          width: self.$refs.img.naturalWidth,
          height: self.$refs.img.naturalHeight,
          ratio: self.$refs.img.naturalHeight / self.$refs.img.naturalWidth
        }
      })
    },
    'shown.width': function () {
      this.shown.height = this.origin.ratio * this.shown.width
      this.shown.scale = this.shown.width / this.origin.width
    },
    'origin': function () {
      this.shown.height = this.origin.ratio * this.shown.width
      this.shown.scale = this.shown.width / this.origin.width
    }
  }
}
</script>

<template>
  <div class="flex grow container-fluid p-0 h-left" tabindex="0"
    @keyup.right="updownimage(1)"
    @keyup.left="updownimage(-1)"
    @keyup.up="contoursSelect(-1)"
    @keyup.down="contoursSelect(1)"
    @keyup.space="showPanel = !showPanel">
    <window-event v-if="drag"
      @mousemove="
        drag.diffX = $event.clientX - drag.orgX
        drag.diffY = $event.clientY - drag.orgY"
      @mouseup="
        shown.left += drag.diffX
        shown.top += drag.diffY
        drag = null"/>

    <div class="grow flex p-0" :class="showPanel ? ['col-md-8'] : ['col-md-12'] ">
      <div class="flex">
        <div class="p-1 px-3 bg-dark flex between h-left">
          <h5 class="text-light mt-1">{{selectedLabel}}</h5>
          <div style="width: 20px; ">
            <input type="checkbox" v-model="showPanel" class="form-control"></div>
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
          <svg :viewBox="viewBox" xmlns="http://www.w3.org/2000/svg" class="frame" v-if="viewBox && selectedControus">
            <!-- <polyline v-for="(contour, conkey) in selectedControus" :key="conkey" v-if=""
              :points="contour.map(p => p.map(c => parseInt(c * shown.scale)).join(',')).join(' ')"
              style="fill:none;stroke:green;stroke-width:1"/> -->
            <polyline v-if="selectedControus"
            :points="selectedControus.map(p => p.map(c => parseInt(c * shown.scale)).join(',')).join(' ')"
            style="fill:none;stroke:red;stroke-width:1"/>
          </svg>
        </div>
      </div>
      <div class="bg-dark" style="overflow-x: scroll;">
        <img
          @click="selectedidx = i"
          :src="rHost + '/static/' + (typeof img === 'string'? img : img['image'])"
          v-for="(img, i) in images" :key="i"
          style="height: 80px; width: 60px;"
          :class="selectedidx == i ? ['border', 'border-light'] : []"
          />
      </div>
    </div>
    <contour class="flex grow col-md-4" v-show="showPanel"
      :contourdataes="contourdataes" ref="contour"
      @selected="selectedControus = $event"/>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Contour from '@/comp/Contour'

export default {
  props: {
    images: { type: Array, default: () => [] },
    contourdataes: { type: Array, default: () => [] }
  },
  data () {
    return {
      viewBox: '',
      selectedControus: null,
      selectedidx: 0,
      selected: null,
      selectedLabel: '무제',
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
      drag: null,
      showPanel: false,
    }
  },
  mounted () {

  },
  computed: {
    ...mapState(['rHost']),
  },
  methods: {
    updownimage (add) {
      if (this.selectedidx + add >= this.images.length) {
        this.selectedidx = 0
      } else if (this.selectedidx + add < 0) {
        this.selectedidx = this.images.length - 1
      } else this.selectedidx = this.selectedidx + add
    },
    contoursSelect (add) {
      this.$refs.contour.$emit('select', add)
    }
  },
  watch: {
    images () {
      if (this.images.length > 0) {
        if (typeof this.images[0] === 'string') {
          this.selectedLabel = this.images[0]
          this.selected = this.images[0]
        } else {
          var obj = this.images[0]
          this.selectedLabel = obj['name']
          this.selected = obj['image']
        }
      } else {
        this.selected = null
      }
    },
    selectedidx () {
      if (this.images.length > 0) {
        if (typeof this.images[0] === 'string') {
          this.selectedLabel = this.images[this.selectedidx]
          this.selected = this.images[this.selectedidx]
        } else {
          var obj = this.images[this.selectedidx]
          this.selectedLabel = obj['name']
          this.selected = obj['image']
        }
      } else {
        this.selected = null
        this.selectedLabel = '무제'
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
      this.viewBox = `0 0 ${this.shown.width} ${this.shown.height}`
    },
    'origin': function () {
      this.shown.height = this.origin.ratio * this.shown.width
      this.shown.scale = this.shown.width / this.origin.width
      this.viewBox = `0 0 ${this.shown.width} ${this.shown.height}`
    }
  },
  components: { Contour }
}
</script>

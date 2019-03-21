<template>
  <div class="flex grow">
    <div class="flex grow y-scroll">
      <filter-cell ref="src"
        title="#1. src"
        description="원본이미지입니다."
        :visible="output.src"
        :property="{
          width: 10000,
          height: 10000
        }"
        @toggle-visible="output.src = !output.src"
        />

     <filter-cell
        title="#3. gray"
        description="이미지를 그레이 스케일로 변환합니다."
        :visible="output.gray"
        @toggle-visible="output.gray = !output.gray" />


      <filter-cell
        title="#5. cany"
        description="윤곽선을 검출시킵니다."
        :visible="output.cany"
        @toggle-visible="output.cany = !output.cany" />


      <filter-cell
        title="#7. contours"
        description="마지막으로 콘트라를 따옵니다."
        :visible="output.contours"
        @toggle-visible="output.contours = !output.contours" />

      
    </div>

    

    <div class="flex h-right">
      <button class="btn btn-primary">Apply</button>
    </div>
  </div>
</template>

<script>
import Toggle from '@/comp/Toggle'
import FilterCell from '@/comp/FilterCell'

export default {
  data() {
    return {
      list: {
        preblur: [],
        postblur: [],
        mono: []
      },
      output: {
        src: false,
        gray: false,
        cany: false,
        contours: false
      }
    }
  },
  mounted () {
    
  },
  components: { Toggle, FilterCell }
}
</script>

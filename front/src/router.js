import Vue from 'vue'
import Router from 'vue-router'

import MakeFilter from '@/pages/MakeFilter'
import ListSource from '@/pages/ListSource'
import ModifyPoly from '@/pages/ModifyPoly'
import RealtimeBander from '@/pages/RealtimeBander'
import GoRun from '@/pages/GoRun'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: ListSource
    },
    {
      path: '/makefilter',
      component: MakeFilter
    },
    {
      path: '/modify-poly',
      component: ModifyPoly
    },
    {
      path: '/realtime-bander',
      component: RealtimeBander
    },
    {
      path: '/go-run',
      component: GoRun
    }
  ]
})

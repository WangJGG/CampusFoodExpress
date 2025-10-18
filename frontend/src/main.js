import { createApp } from 'vue'
import { createPinia } from 'pinia'
import {
    ActionBar, ActionBarIcon, ActionBarButton, Divider, Popup, Overlay,
    Loading, Dialog, ContactCard, Form, AddressEdit, AddressList, Field,
    CellGroup, Cell, SwipeCell, Icon, Stepper, Card, Checkbox, CheckboxGroup,
    Button, Swipe, SwipeItem, PullRefresh, List, Tab, Tabs, SubmitBar, Toast, Tabbar, TabbarItem,
    Skeleton
} from 'vant'
import ArcoVue from "@arco-design/web-vue";
import "@arco-design/web-vue/dist/arco.css";

import App from './App.vue'
import router from './router'

import 'lib-flexible/flexible'
import './assets/main.css'
import './assets/global.css';  // 引入全局CSS
import 'vant/es/toast/style'
import 'vant/lib/index.css';
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
    faUser, faLock, faChartBar, faComment, faGift, faPhone, faUserTie,
    faArrowLeft, faReceipt, faInfoCircle, faCalendarAlt, faCheckCircle,
    faDollarSign, faClock, faListUl, faUserCircle, faStore, faStoreAlt,
    faMapMarkerAlt, faPhoneSquareAlt, faPaw, faCircleExclamation
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(
    faUser, faLock, faChartBar, faComment, faGift, faPhone, faUserTie,
    faArrowLeft, faReceipt, faInfoCircle, faCalendarAlt, faCheckCircle,
    faDollarSign, faClock, faListUl, faUserCircle, faStore, faStoreAlt,
    faMapMarkerAlt, faPhoneSquareAlt, faPaw, faCircleExclamation
);

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ActionBarButton)
    .use(ActionBarIcon)
    .use(ActionBar)
    .use(ArcoVue)
    .use(Divider)
    .use(Popup)
    .use(Overlay)
    .use(Loading)
    .use(Dialog)
    .use(Toast)
    .use(ContactCard)
    .use(Form)
    .use(AddressEdit)
    .use(AddressList)
    .use(Field)
    .use(CellGroup)
    .use(Cell)
    .use(SwipeCell)
    .use(Icon)
    .use(Stepper)
    .use(Card)
    .use(Button)
    .use(Swipe)
    .use(SwipeItem)
    .use(PullRefresh)
    .use(List)
    .use(Tab)
    .use(Tabs)
    .use(SubmitBar)
    .use(Checkbox)
    .use(CheckboxGroup)
    .use(Skeleton)
    .use(Tabbar)
    .use(TabbarItem)
    .use(ElementPlus)



app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')


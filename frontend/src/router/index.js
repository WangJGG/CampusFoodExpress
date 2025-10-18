/* eslint-disable */
import { createRouter, createWebHashHistory } from 'vue-router'
import mainPage from '@/views/mainPage.vue'
import userPage from '@/views/userPage.vue'
import userProfile from '@/views/userProfile.vue'
import userPassword from '@/views/userPassword.vue'
import userAuthentication from '@/views/userAuthentication.vue'
import userLogin from '@/views/userLogin.vue'
import userRegister from '@/views/userRegister.vue'
import foodMap from '@/views/foodMap.vue'
import orderDetail from '@/views/orderDetail.vue'
import foodOrder from '@/views/foodOrder.vue'
import rewardPublish from "@/views/rewardPublish.vue"; // 新的悬赏发布页面
import merchantRate from '@/views/merchantRate.vue'
import restaurantTrack from '@/views/restaurantTrack.vue'
import userInfo from "@/views/userInfo.vue"; // 用户详情页面
import groupDetail from '@/views/groupDetail.vue'
import addGroupMember from '@/views/addGroupMember.vue'
import "@arco-design/web-vue/dist/arco.css";

import merchantDetail from '@/views/merchantDetail.vue'
import addAddress from '@/views/addAddress.vue';
import "@arco-design/web-vue/dist/arco.css";

//userLikes
import UserLikes from '@/views/userLikes.vue';
//userAccusion
import UserAccusation from '@/views/userAccusation.vue';
//userStatus
import UserStatus from '@/components/userStatus.vue';
import StatusDetail from '@/views/statusDetail.vue';
//userComment
import UserComments from '@/views/userComments.vue';
import DetailComments from '@/views/detailComments.vue';
import chatPage from '@/views/chatPage.vue'
//userInfo
// import UserInfo from '@/views/userInfo.vue';
import sysDetailNotification from '@/views/sysDetailNotification.vue'
import orderDetailNotification from '@/views/orderDetailNotification.vue'

import creategroup from '@/views/createGroup.vue'

import findFriend from '@/views/findFriend.vue'

// 获取 token 方法（可以从 localStorage、sessionStorage 或 Vuex 中获取）
const getToken = () => localStorage.getItem('token'); // 根据实际存储方式调整

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/main',
            name: 'main',
            component: mainPage,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/login',
            name: 'Login',
            component: userLogin,
            meta: {
                requiresAuth: false
            }
        },
        {
            path: '/register',
            name: 'Register',
            component: userRegister,
            meta: {
                requiresAuth: false
            }
        },
        
        // user
        {
            path: '/userPage',
            name: 'userPage',
            component: userPage,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/userProfile',
            name: 'userProfile',
            component: userProfile,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/userPassword',
            name: 'userPassword',
            component: userPassword,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/userAuthentication',
            name: 'userAuthentication',
            component: userAuthentication,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/userInfo',
            name: 'userInfo',
            component: userInfo,
            meta: {
                requiresAuth: true
            }
        },
        //userLikes
        {
            path: '/userLikes',
            name: 'UserLikes',
            component: UserLikes,
            meta: {
                requiresAuth: true
            }
        },
        //userAccusation
        {
            path: '/userAccusation',
            name: 'UserAccusation',
            component: UserAccusation,
            meta: {
                requiresAuth: true
            }
        },
        //userStatus
        {
            path: '/userStatus',
            component: UserStatus,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/statusDetail',
            component: StatusDetail,
            meta: {
                requiresAuth: true
            }
        },

        {
            path: '/merchantDetail',
            name: 'merchantDetail',
            component: merchantDetail,
            props: true,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/foodMap',
            name: 'foodMap',
            component: foodMap,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/orderDetail',
            name: 'orderDetail',
            component: orderDetail,
            meta: {
                requiresAuth: true
            }
        },

        {
            path: '/foodOrder',
            name: 'foodOrder',
            component: foodOrder,
            meta: {
                requiresAuth: true
            }
        },

        {
            path: '/rewardPublish',
            name: 'rewardPublish',
            component: rewardPublish,
            meta: {
                requiresAuth: true
            }
        },

        {
            path: '/addAddress',
            name: 'addAddress',
            component: addAddress,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/detailComments',
            name: 'detailComments',
            component: DetailComments,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/userComments',
            name: 'userComments',
            component: UserComments,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/merchantRate',
            name: 'merchantRate',
            component: merchantRate,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/friends',
            name: 'familyList',
            component: () => import('@/views/familyList.vue'),
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/sysNotificationDetail',
            name: 'sysDetailNotification',
            component: sysDetailNotification,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/orderNotificationDetail',
            name: 'orderDetailNotification',
            component: orderDetailNotification,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/creategroup',
            name: 'creategroup',
            component: creategroup,
            meta: {
                requiresAuth: true
            }
        },

        {
            path: '/restaurantTrack',
            name: 'restaurantTrack',
            component: restaurantTrack,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/chatPage',
            name: 'chatPage',
            component: chatPage,
        },
        {
            path: '/chatPage',
            name: 'chatPage',
            component: chatPage,
        },
        {
            path: '/groupDetail',
            name: 'groupDetail',
            component: groupDetail,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/findFriend',
            name: 'findFriend',
            component: findFriend,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/addGroupMember',
            name: 'addGroupMember',
            component: addGroupMember,
            meta: {
                requiresAuth: true
            }
        },
    ]
})

// 全局路由前置守卫
router.beforeEach((to, from, next) => {
    const token = getToken(); // 获取 token

    if (to.meta.requiresAuth && !token) {
        // 如果目标路由需要登录权限，且没有 token，跳转到登录页
        next({ path: '/login' });
    } else {
        // 如果有 token 或目标路由不需要权限，继续导航
        next();
    }
});

export default router
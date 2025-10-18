import { createRouter, createWebHashHistory } from 'vue-router'
import "@arco-design/web-vue/dist/arco.css";

import comment from '@/views/adminComment.vue'
import adminPage from '@/views/adminPage.vue'
import realNameAuthentication from '@/views/adminRealNameAuthentication.vue'
import reportHandlinig from '@/views/adminReportHandlinig.vue'
import restaurantAcount from '@/views/adminRestaurantAcount.vue'
import userAcount from '@/views/adminUserAcount.vue'
import LoginRegister from '@/views/register-login.vue'

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
            path: '/login',
            name: 'Login',
            component: LoginRegister,
            meta: {
                index: 1
            }
        },
        // admin
        {
            path: '/admin',
            name: 'admin',
            component: adminPage,
            meta: {
                index: 1,
                requiresAuth: true
            }
        },
        {
            path: '/restaurantAcount',
            name: 'restaurantAcount',
            component: restaurantAcount,
            meta: {
                index: 1,
                requiresAuth: true
            }
        },
        {
            path: '/realNameAuthentication',
            name: 'realNameAuthentication',
            component: realNameAuthentication,
            meta: {
                index: 1,
                requiresAuth: true
            }
        },
        {
            path: '/reportHandlinig',
            name: 'reportHandlinig',
            component: reportHandlinig,
            meta: {
                index: 1,
                requiresAuth: true
            }
        },
        {
            path: '/comment',
            name: 'comment',
            component: comment,
            meta: {
                index: 1,
                requiresAuth: true
            }
        },
        {
            path: '/userAcount',
            name: 'userAcount',
            component: userAcount,
            meta: {
                index: 1,
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
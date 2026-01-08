import { createRouter, createWebHistory } from 'vue-router';
import ItemListPage from '../pages/ItemListPage.vue';
import ItemDetailPage from '../pages/ItemDetailPage.vue';
import NewItemPage from '../pages/NewItemPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import { useAuthStore } from '../stores/auth';
import { pinia } from '../stores';

const base = import.meta.env.MODE === 'development' ? import.meta.env.BASE_URL : '';

const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', redirect: '/items' },
        { path: '/items', name: 'Item List', component: ItemListPage },
        { path: '/items/new', name: 'New Item', component: NewItemPage, meta: { requiresAuth: true } },
        { path: '/items/:id', name: 'Item Detail', component: ItemDetailPage, props: true },
        { path: '/profile', name: 'Profile', component: ProfilePage, meta: { requiresAuth: true } },
    ],
});

router.beforeEach((to) => {
    if (to.meta.requiresAuth) {
        const authStore = useAuthStore(pinia);
        if (!authStore.isAuthenticated) {
            return { path: '/items' };
        }
    }
    return true;
});

export default router;

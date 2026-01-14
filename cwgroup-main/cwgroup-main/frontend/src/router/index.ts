import { createRouter, createWebHashHistory } from 'vue-router';
import ItemListPage from '../pages/ItemListPage.vue';
import ItemDetailPage from '../pages/ItemDetailPage.vue';
import NewItemPage from '../pages/NewItemPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import { useAuthStore } from '../stores/auth';
import { pinia } from '../stores';

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: '/', redirect: '/items' },
        { path: '/items', name: 'Item List', component: ItemListPage },
        { path: '/items/new', name: 'New Item', component: NewItemPage, meta: { requiresAuth: true } },
        { path: '/items/:id', name: 'Item Detail', component: ItemDetailPage, props: true },
        { path: '/profile', name: 'Profile', component: ProfilePage, meta: { requiresAuth: true } },
    ],
});

router.beforeEach(async (to) => {
    if (to.meta.requiresAuth) {
        const authStore = useAuthStore(pinia);
        if (!authStore.isAuthenticated) {
            await authStore.fetchProfile();
        }
        if (!authStore.isAuthenticated) {
            const nextPath = `/#${to.fullPath}`;
            window.location.assign(`/accounts/login/?next=${encodeURIComponent(nextPath)}`);
            return false;
        }
    }
    return true;
});

export default router;

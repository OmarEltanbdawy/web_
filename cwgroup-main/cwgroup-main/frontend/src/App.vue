<template>
    <main class="container py-4">
        <header class="d-flex flex-wrap align-items-center justify-content-between mb-4">
            <h1 class="h4 mb-0">Auction House</h1>
            <nav class="d-flex gap-3">
                <RouterLink class="text-decoration-none" to="/items">Items</RouterLink>
                <RouterLink
                    v-if="authStore.isAuthenticated"
                    class="text-decoration-none"
                    to="/items/new"
                >
                    New Item
                </RouterLink>
                <a
                    v-else
                    class="text-decoration-none"
                    :href="loginUrl('/items/new')"
                >
                    New Item
                </a>
                <RouterLink
                    v-if="authStore.isAuthenticated"
                    class="text-decoration-none"
                    to="/profile"
                >
                    Profile
                </RouterLink>
                <a
                    v-else
                    class="text-decoration-none"
                    :href="loginUrl('/profile')"
                >
                    Profile
                </a>
            </nav>
        </header>
        <RouterView />
    </main>
</template>

<script lang="ts" setup>
import { RouterLink, RouterView } from 'vue-router';
import { useAuthStore } from './stores/auth';

const authStore = useAuthStore();
const loginUrl = (path: string) => `/accounts/login/?next=${encodeURIComponent(`/#${path}`)}`;
</script>

<template>
    <main class="container py-4">
        <header class="d-flex flex-wrap align-items-center justify-content-between mb-4">
            <h1 class="h4 mb-0">Auction House</h1>
            <nav class="d-flex gap-3">
                <RouterLink class="text-decoration-none" to="/items">Items</RouterLink>
                <RouterLink class="text-decoration-none" to="/items/new">New Item</RouterLink>
                <RouterLink class="text-decoration-none" to="/profile">Profile</RouterLink>
            </nav>
        </header>
        <RouterView />
    </main>
</template>

<script lang="ts" setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

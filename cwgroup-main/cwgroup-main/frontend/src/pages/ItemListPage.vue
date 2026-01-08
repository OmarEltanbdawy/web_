<template>
    <section>
        <div class="d-flex align-items-center justify-content-between mb-3">
            <h2 class="h5 mb-0">Available Items</h2>
            <button class="btn btn-outline-secondary btn-sm" @click="refreshItems">Refresh</button>
        </div>

        <div v-if="auctionStore.isLoading" class="alert alert-info">Loading items...</div>
        <div v-else-if="auctionStore.errorMessage" class="alert alert-danger">
            {{ auctionStore.errorMessage }}
        </div>

        <ul v-else class="list-group">
            <li v-for="item in auctionStore.items" :key="item.id" class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h3 class="h6 mb-1">{{ item.title }}</h3>
                        <p class="mb-0 text-muted">Current bid: ${{ item.currentPrice }}</p>
                    </div>
                    <RouterLink class="btn btn-primary btn-sm" :to="`/items/${item.id}`">
                        View
                    </RouterLink>
                </div>
            </li>
        </ul>
    </section>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuctionStore } from '../stores/auction';

const auctionStore = useAuctionStore();

const refreshItems = () => {
    auctionStore.loadItems();
};

onMounted(() => {
    refreshItems();
});
</script>

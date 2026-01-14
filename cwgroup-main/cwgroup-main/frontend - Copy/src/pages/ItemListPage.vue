<template>
    <section>
        <div class="d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-2 mb-3">
            <h2 class="h5 mb-0">Available Items</h2>
            <div class="d-flex gap-2">
                <input
                    v-model="searchTerm"
                    class="form-control form-control-sm"
                    style="max-width: 260px"
                    placeholder="Search items..."
                    @input="scheduleSearch"
                />
                <button class="btn btn-outline-secondary btn-sm" @click="refreshItems">Refresh</button>
            </div>
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
                        <p class="mb-0 text-muted">
                            Starting price: ${{ item.startingPrice.toFixed(2) }}
                            <span v-if="item.hasEnded" class="badge bg-secondary ms-2">Ended</span>
                        </p>
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
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuctionStore } from '../stores/auction';

const auctionStore = useAuctionStore();
const searchTerm = ref('');
let searchTimeout: number | undefined;

const refreshItems = () => {
    auctionStore.loadItems();
};

const scheduleSearch = () => {
    if (searchTimeout) {
        window.clearTimeout(searchTimeout);
    }
    searchTimeout = window.setTimeout(() => {
        auctionStore.loadItems(searchTerm.value.trim());
    }, 300);
};

onMounted(() => {
    refreshItems();
});
</script>

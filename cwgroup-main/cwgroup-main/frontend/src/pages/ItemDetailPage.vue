<template>
    <section>
        <div v-if="auctionStore.isLoading" class="alert alert-info">Loading item...</div>
        <div v-else-if="auctionStore.errorMessage" class="alert alert-danger">
            {{ auctionStore.errorMessage }}
        </div>

        <div v-else-if="auctionStore.selectedItem" class="card">
            <div class="card-body">
                <h2 class="h5">{{ auctionStore.selectedItem.title }}</h2>
                <p class="text-muted">{{ auctionStore.selectedItem.description }}</p>
                <p class="mb-1">Current price: ${{ auctionStore.selectedItem.currentPrice }}</p>
                <p class="mb-0">Ends at: {{ auctionStore.selectedItem.endsAt }}</p>
            </div>
        </div>

        <div class="mt-4">
            <h3 class="h6">Questions</h3>
            <ul class="list-group">
                <li
                    v-for="question in auctionStore.questions"
                    :key="question.id"
                    class="list-group-item"
                >
                    {{ question.body }}
                </li>
            </ul>
        </div>
    </section>
</template>

<script lang="ts" setup>
import { onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useAuctionStore } from '../stores/auction';

const route = useRoute();
const auctionStore = useAuctionStore();

const loadItem = () => {
    const id = Number(route.params.id);
    if (!Number.isNaN(id)) {
        auctionStore.loadItem(id);
    }
};

onMounted(loadItem);
watch(() => route.params.id, loadItem);
</script>

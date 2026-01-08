<template>
    <section class="card">
        <div class="card-body">
            <h2 class="h5">Create New Item</h2>
            <form class="mt-3" @submit.prevent="submit">
                <div class="mb-3">
                    <label class="form-label" for="title">Title</label>
                    <input id="title" v-model="form.title" class="form-control" required />
                </div>
                <div class="mb-3">
                    <label class="form-label" for="description">Description</label>
                    <textarea id="description" v-model="form.description" class="form-control" rows="3" required></textarea>
                </div>
                <div class="mb-3">
                    <label class="form-label" for="price">Starting Price</label>
                    <input
                        id="price"
                        v-model.number="form.startingPrice"
                        class="form-control"
                        type="number"
                        min="0"
                        step="0.01"
                        required
                    />
                </div>
                <div class="mb-3">
                    <label class="form-label" for="endsAt">Ends At</label>
                    <input id="endsAt" v-model="form.endsAt" class="form-control" type="datetime-local" required />
                </div>
                <div class="d-flex gap-2">
                    <button class="btn btn-primary" type="submit" :disabled="auctionStore.isLoading">
                        Save Item
                    </button>
                    <span v-if="auctionStore.errorMessage" class="text-danger">
                        {{ auctionStore.errorMessage }}
                    </span>
                </div>
            </form>
        </div>
    </section>
</template>

<script lang="ts" setup>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuctionStore } from '../stores/auction';

const router = useRouter();
const auctionStore = useAuctionStore();

const form = reactive({
    title: '',
    description: '',
    startingPrice: 0,
    endsAt: '',
});

const submit = async () => {
    const item = await auctionStore.createNewItem({
        title: form.title,
        description: form.description,
        startingPrice: form.startingPrice,
        endsAt: form.endsAt,
    });

    if (item) {
        router.push(`/items/${item.id}`);
    }
};
</script>

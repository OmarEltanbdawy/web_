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
                    <div v-if="endTimeError" class="text-danger small mt-1">{{ endTimeError }}</div>
                </div>
                <div class="mb-3">
                    <label class="form-label" for="image">Item Image</label>
                    <input
                        id="image"
                        class="form-control"
                        type="file"
                        accept="image/*"
                        @change="handleImageChange"
                    />
                    <img
                        v-if="imagePreview"
                        :src="imagePreview"
                        alt="Preview"
                        class="img-thumbnail mt-2"
                        style="max-width: 220px"
                    />
                </div>
                <div class="d-flex gap-2">
                    <button class="btn btn-primary" type="submit" :disabled="auctionStore.isLoading || !!endTimeError">
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
import { computed, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuctionStore } from '../stores/auction';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const auctionStore = useAuctionStore();
const authStore = useAuthStore();
const imagePreview = ref<string | null>(null);

const form = reactive({
    title: '',
    description: '',
    startingPrice: 0,
    endsAt: '',
});

const endTimeError = computed(() => {
    if (!form.endsAt) {
        return '';
    }
    const endDate = new Date(form.endsAt);
    if (Number.isNaN(endDate.getTime())) {
        return 'Please enter a valid end time.';
    }
    if (endDate <= new Date()) {
        return 'End time must be in the future.';
    }
    return '';
});

const handleImageChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0] || null;
    imagePreview.value = file ? URL.createObjectURL(file) : null;
};

const submit = async () => {
    if (!authStore.user) {
        auctionStore.errorMessage = 'Please sign in to create an item.';
        return;
    }
    if (endTimeError.value) {
        return;
    }
    const item = await auctionStore.createNewItem({
        ownerId: authStore.user.id,
        title: form.title,
        description: form.description,
        startingPrice: form.startingPrice,
        endTime: new Date(form.endsAt).toISOString(),
    });

    if (item) {
        router.push(`/items/${item.id}`);
    }
};
</script>

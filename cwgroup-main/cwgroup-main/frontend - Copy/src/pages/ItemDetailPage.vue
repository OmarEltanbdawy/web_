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
                <p class="mb-1">
                    Current price: ${{ currentPrice.toFixed(2) }}
                    <span v-if="auctionStore.selectedItem.hasEnded" class="badge bg-secondary ms-2">Ended</span>
                </p>
                <p class="mb-0">Ends at: {{ formatDate(auctionStore.selectedItem.endTime) }}</p>
            </div>
        </div>

        <div v-if="auctionStore.selectedItem" class="row g-4 mt-4">
            <div class="col-lg-6">
                <div class="card h-100">
                    <div class="card-body">
                        <h3 class="h6">Place a Bid</h3>
                        <p class="text-muted small mb-2">
                            Minimum bid: ${{ minimumBid.toFixed(2) }}
                        </p>
                        <form @submit.prevent="submitBid">
                            <div class="input-group mb-2">
                                <span class="input-group-text">$</span>
                                <input
                                    v-model.number="bidAmount"
                                    class="form-control"
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    :disabled="auctionStore.selectedItem.hasEnded"
                                    required
                                />
                            </div>
                            <div v-if="bidError" class="text-danger small mb-2">{{ bidError }}</div>
                            <button class="btn btn-primary btn-sm" type="submit" :disabled="isBidDisabled">
                                Submit Bid
                            </button>
                        </form>
                    </div>
                </div>
                <div class="card mt-4">
                    <div class="card-body">
                        <h3 class="h6">Bid History</h3>
                        <ul class="list-group list-group-flush">
                            <li v-if="!auctionStore.selectedItem.bids.length" class="list-group-item text-muted">
                                No bids yet.
                            </li>
                            <li
                                v-for="bid in auctionStore.selectedItem.bids"
                                :key="bid.id"
                                class="list-group-item d-flex justify-content-between"
                            >
                                <span>User #{{ bid.bidderId }}</span>
                                <span>${{ bid.amount.toFixed(2) }}</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-body">
                        <h3 class="h6">Questions & Answers</h3>
                        <form class="mb-3" @submit.prevent="submitQuestion">
                            <textarea
                                v-model="questionText"
                                class="form-control mb-2"
                                rows="3"
                                placeholder="Ask a question..."
                                required
                            ></textarea>
                            <button class="btn btn-outline-primary btn-sm" type="submit" :disabled="auctionStore.isLoading">
                                Post Question
                            </button>
                        </form>
                        <ul class="list-group">
                            <li
                                v-for="question in auctionStore.selectedItem.questions"
                                :key="question.id"
                                class="list-group-item"
                            >
                                <p class="mb-1"><strong>Q:</strong> {{ question.text }}</p>
                                <p v-if="question.answer" class="mb-2 text-success">
                                    <strong>A:</strong> {{ question.answer.text }}
                                </p>
                                <form
                                    v-else
                                    class="d-flex gap-2"
                                    @submit.prevent="submitAnswer(question.id)"
                                >
                                    <input
                                        v-model="answerDrafts[question.id]"
                                        class="form-control form-control-sm"
                                        placeholder="Write an answer..."
                                        required
                                    />
                                    <button class="btn btn-outline-secondary btn-sm" type="submit">
                                        Reply
                                    </button>
                                </form>
                            </li>
                            <li v-if="!auctionStore.selectedItem.questions.length" class="list-group-item text-muted">
                                No questions yet.
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useAuctionStore } from '../stores/auction';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const auctionStore = useAuctionStore();
const authStore = useAuthStore();
const bidAmount = ref(0);
const questionText = ref('');
const answerDrafts = reactive<Record<number, string>>({});

const currentPrice = computed(() => {
    const item = auctionStore.selectedItem;
    if (!item) {
        return 0;
    }
    const highestBid = item.bids.reduce((max, bid) => Math.max(max, bid.amount), item.startingPrice);
    return highestBid;
});

const minimumBid = computed(() => currentPrice.value);

const bidError = computed(() => {
    const item = auctionStore.selectedItem;
    if (!item) {
        return '';
    }
    if (item.hasEnded) {
        return 'Auction has ended.';
    }
    if (bidAmount.value === 0) {
        return '';
    }
    if (bidAmount.value <= minimumBid.value) {
        return `Bid must be higher than $${minimumBid.value.toFixed(2)}.`;
    }
    return '';
});

const isBidDisabled = computed(() => {
    const item = auctionStore.selectedItem;
    if (!item) {
        return true;
    }
    if (auctionStore.isLoading || item.hasEnded) {
        return true;
    }
    return bidAmount.value <= minimumBid.value;
});

const formatDate = (value: string) => new Date(value).toLocaleString();

const loadItem = () => {
    const id = Number(route.params.id);
    if (!Number.isNaN(id)) {
        auctionStore.loadItem(id);
    }
};

onMounted(loadItem);
watch(() => route.params.id, loadItem);

const submitBid = async () => {
    if (!auctionStore.selectedItem || !authStore.user) {
        auctionStore.errorMessage = 'Please sign in to place a bid.';
        return;
    }
    if (bidError.value) {
        return;
    }
    await auctionStore.submitBid(auctionStore.selectedItem.id, authStore.user.id, bidAmount.value);
    bidAmount.value = 0;
};

const submitQuestion = async () => {
    if (!auctionStore.selectedItem || !authStore.user) {
        auctionStore.errorMessage = 'Please sign in to post a question.';
        return;
    }
    if (!questionText.value.trim()) {
        return;
    }
    await auctionStore.submitQuestion(
        auctionStore.selectedItem.id,
        authStore.user.id,
        questionText.value.trim(),
    );
    questionText.value = '';
};

const submitAnswer = async (questionId: number) => {
    if (!auctionStore.selectedItem || !authStore.user) {
        auctionStore.errorMessage = 'Please sign in to answer questions.';
        return;
    }
    const text = (answerDrafts[questionId] || '').trim();
    if (!text) {
        return;
    }
    await auctionStore.submitAnswer(questionId, authStore.user.id, auctionStore.selectedItem.id, text);
    answerDrafts[questionId] = '';
};
</script>

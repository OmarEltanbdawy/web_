import { defineStore } from 'pinia';
import { createItem, getItem, getItems, placeBid, postAnswer, postQuestion } from '../api/auction';
import { AuthRequiredError } from '../api/client';
import type { ItemDetail, ItemSummary } from '../types';

export const useAuctionStore = defineStore('auction', {
    state: () => ({
        items: [] as ItemSummary[],
        selectedItem: null as ItemDetail | null,
        isLoading: false,
        errorMessage: null as string | null,
    }),
    actions: {
        async loadItems(query?: string) {
            this.isLoading = true;
            this.errorMessage = null;
            try {
                const response = await getItems(query);
                this.items = response.items;
            } catch (error) {
                this.errorMessage = error instanceof Error ? error.message : 'Unable to load items.';
            } finally {
                this.isLoading = false;
            }
        },
        async loadItem(itemId: number) {
            this.isLoading = true;
            this.errorMessage = null;
            try {
                const response = await getItem(itemId);
                this.selectedItem = response.item;
            } catch (error) {
                this.errorMessage = error instanceof Error ? error.message : 'Unable to load item.';
            } finally {
                this.isLoading = false;
            }
        },
        async createNewItem(payload: {
            ownerId: number;
            title: string;
            description: string;
            startingPrice: number;
            endTime: string;
        }) {
            this.isLoading = true;
            this.errorMessage = null;
            try {
                const created = await createItem(payload);
                const response = await getItem(created.id);
                this.items = [response.item, ...this.items];
                return response.item;
            } catch (error) {
                if (error instanceof AuthRequiredError) {
                    this.errorMessage = 'Please sign in to create an item.';
                    return null;
                }
                this.errorMessage = error instanceof Error ? error.message : 'Unable to create item.';
                return null;
            } finally {
                this.isLoading = false;
            }
        },
        async submitBid(itemId: number, bidderId: number, amount: number) {
            this.isLoading = true;
            this.errorMessage = null;
            try {
                await placeBid(itemId, { bidderId, amount });
                const response = await getItem(itemId);
                this.selectedItem = response.item;
                return true;
            } catch (error) {
                if (error instanceof AuthRequiredError) {
                    this.errorMessage = 'Please sign in to place a bid.';
                    return false;
                }
                this.errorMessage = error instanceof Error ? error.message : 'Unable to place bid.';
                return false;
            } finally {
                this.isLoading = false;
            }
        },
        async submitQuestion(itemId: number, askerId: number, text: string) {
            this.isLoading = true;
            this.errorMessage = null;
            try {
                await postQuestion(itemId, { askerId, text });
                const response = await getItem(itemId);
                this.selectedItem = response.item;
                return true;
            } catch (error) {
                if (error instanceof AuthRequiredError) {
                    this.errorMessage = 'Please sign in to ask a question.';
                    return false;
                }
                this.errorMessage = error instanceof Error ? error.message : 'Unable to post question.';
                return false;
            } finally {
                this.isLoading = false;
            }
        },
        async submitAnswer(questionId: number, responderId: number, itemId: number, text: string) {
            this.isLoading = true;
            this.errorMessage = null;
            try {
                await postAnswer(questionId, { responderId, text });
                const response = await getItem(itemId);
                this.selectedItem = response.item;
                return true;
            } catch (error) {
                if (error instanceof AuthRequiredError) {
                    this.errorMessage = 'Please sign in to answer questions.';
                    return false;
                }
                this.errorMessage = error instanceof Error ? error.message : 'Unable to post answer.';
                return false;
            } finally {
                this.isLoading = false;
            }
        },
    },
});

import { defineStore } from 'pinia';
import { createItem, getItem, getItems } from '../api/auction';
import { AuthRequiredError } from '../api/client';
import type { Item, Question } from '../types';

export const useAuctionStore = defineStore('auction', {
    state: () => ({
        items: [] as Item[],
        selectedItem: null as Item | null,
        questions: [] as Question[],
        isLoading: false,
        errorMessage: null as string | null,
    }),
    actions: {
        async loadItems() {
            this.isLoading = true;
            this.errorMessage = null;
            try {
                const response = await getItems();
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
                this.questions = response.questions;
            } catch (error) {
                this.errorMessage = error instanceof Error ? error.message : 'Unable to load item.';
            } finally {
                this.isLoading = false;
            }
        },
        async createNewItem(payload: {
            title: string;
            description: string;
            startingPrice: number;
            endsAt: string;
        }) {
            this.isLoading = true;
            this.errorMessage = null;
            try {
                const item = await createItem(payload);
                this.items = [item, ...this.items];
                return item;
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
    },
});

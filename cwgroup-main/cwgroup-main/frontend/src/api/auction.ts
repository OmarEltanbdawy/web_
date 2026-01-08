import { fetchJson } from './client';
import type { Item, Question } from '../types';

export interface ItemListResponse {
    items: Item[];
}

export interface ItemDetailResponse {
    item: Item;
    questions: Question[];
}

export interface CreateItemPayload {
    title: string;
    description: string;
    startingPrice: number;
    endsAt: string;
}

export const getItems = () => fetchJson<ItemListResponse>('/api/items/');

export const getItem = (itemId: number) => fetchJson<ItemDetailResponse>(`/api/items/${itemId}/`);

export const createItem = (payload: CreateItemPayload) =>
    fetchJson<Item>('/api/items/', {
        method: 'POST',
        body: JSON.stringify(payload),
    });

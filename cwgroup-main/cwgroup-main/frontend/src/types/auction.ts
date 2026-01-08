export interface Item {
    id: number;
    title: string;
    description: string;
    startingPrice: number;
    currentPrice: number;
    endsAt: string;
    sellerId: number;
}

export interface Bid {
    id: number;
    itemId: number;
    bidderId: number;
    amount: number;
    createdAt: string;
}

export interface Question {
    id: number;
    itemId: number;
    authorId: number;
    body: string;
    createdAt: string;
}

export interface Answer {
    id: number;
    questionId: number;
    authorId: number;
    body: string;
    createdAt: string;
}

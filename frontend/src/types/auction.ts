export interface ItemSummary {
    id: number;
    title: string;
    description: string;
    startingPrice: number;
    endTime: string;
    hasEnded: boolean;
}

export interface Bid {
    id: number;
    bidderId: number;
    amount: number;
    createdAt: string;
}

export interface Answer {
    id: number;
    responderId: number;
    text: string;
    createdAt: string;
}

export interface Question {
    id: number;
    askerId: number;
    text: string;
    createdAt: string;
    answer: Answer | null;
}

export interface WinningBid {
    id: number;
    bidderId: number;
    amount: number;
}

export interface ItemDetail extends ItemSummary {
    bids: Bid[];
    questions: Question[];
    winningBid: WinningBid | null;
}

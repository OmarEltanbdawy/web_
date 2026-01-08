export interface UserProfile {
    id: number;
    username: string;
    email?: string;
    displayName?: string;
    joinedAt?: string;
}

export interface AuthContext {
    isAuthenticated: boolean;
    user: UserProfile | null;
}

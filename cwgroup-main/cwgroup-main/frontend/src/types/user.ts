export interface UserProfile {
    id: number;
    username: string;
    email: string;
    firstName: string;
    lastName: string;
    dateOfBirth: string | null;
    profileImageUrl: string | null;
}

export interface AuthContext {
    isAuthenticated: boolean;
    user: UserProfile | null;
}

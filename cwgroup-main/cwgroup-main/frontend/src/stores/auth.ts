import { defineStore } from 'pinia';
import { AuthRequiredError } from '../api/client';
import { getProfile } from '../api/auth';
import type { AuthContext, UserProfile } from '../types';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as UserProfile | null,
        isAuthenticated: false,
        status: 'idle' as 'idle' | 'loading' | 'ready' | 'error',
        errorMessage: null as string | null,
    }),
    actions: {
        bootstrap(context?: AuthContext) {
            if (context) {
                this.user = context.user;
                this.isAuthenticated = context.isAuthenticated;
            }
            this.status = 'ready';
        },
        async fetchProfile() {
            this.status = 'loading';
            this.errorMessage = null;
            try {
                const profile = await getProfile();
                this.user = profile;
                this.isAuthenticated = true;
                this.status = 'ready';
            } catch (error) {
                if (error instanceof AuthRequiredError) {
                    this.user = null;
                    this.isAuthenticated = false;
                    this.status = 'ready';
                    return;
                }
                this.status = 'error';
                this.errorMessage = error instanceof Error ? error.message : 'Unable to load profile.';
            }
        },
    },
});

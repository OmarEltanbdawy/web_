import { defineStore } from 'pinia';
import { AuthRequiredError } from '../api/client';
import { type ApiUserProfile, getProfile, mapUserProfile, updateProfile } from '../api/auth';
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
                this.user = context.user ? mapUserProfile(context.user as ApiUserProfile) : null;
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
        async saveProfile(payload: FormData) {
            this.status = 'loading';
            this.errorMessage = null;
            try {
                const profile = await updateProfile(payload);
                this.user = profile;
                this.status = 'ready';
                return profile;
            } catch (error) {
                this.status = 'error';
                this.errorMessage = error instanceof Error ? error.message : 'Unable to update profile.';
                return null;
            }
        },
    },
});

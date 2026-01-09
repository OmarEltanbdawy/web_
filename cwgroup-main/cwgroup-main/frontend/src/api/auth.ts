import { fetchJson } from './client';
import type { UserProfile } from '../types';

export interface ApiUserProfile {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    date_of_birth: string | null;
    profile_image_url: string | null;
}

export const mapUserProfile = (profile: ApiUserProfile): UserProfile => ({
    id: profile.id,
    username: profile.username,
    email: profile.email,
    firstName: profile.first_name,
    lastName: profile.last_name,
    dateOfBirth: profile.date_of_birth,
    profileImageUrl: profile.profile_image_url,
});

export const getProfile = async () => {
    const profile = await fetchJson<ApiUserProfile>('/accounts/profile/');
    return mapUserProfile(profile);
};

export const updateProfile = async (payload: FormData) => {
    const profile = await fetchJson<ApiUserProfile>('/accounts/profile/update/', {
        method: 'PATCH',
        body: payload,
    });
    return mapUserProfile(profile);
};

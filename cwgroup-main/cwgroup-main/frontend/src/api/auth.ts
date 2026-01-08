import { fetchJson } from './client';
import type { UserProfile } from '../types';

export const getProfile = () => fetchJson<UserProfile>('/api/profile/');

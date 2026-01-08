<template>
    <section>
        <h2 class="h5">Profile</h2>
        <div v-if="authStore.status === 'loading'" class="alert alert-info">Loading profile...</div>
        <div v-else-if="authStore.errorMessage" class="alert alert-danger">
            {{ authStore.errorMessage }}
        </div>
        <div v-else-if="authStore.user" class="card">
            <div class="card-body">
                <p class="mb-1"><strong>Username:</strong> {{ authStore.user.username }}</p>
                <p v-if="authStore.user.email" class="mb-1">
                    <strong>Email:</strong> {{ authStore.user.email }}
                </p>
                <p v-if="authStore.user.displayName" class="mb-0">
                    <strong>Display name:</strong> {{ authStore.user.displayName }}
                </p>
            </div>
        </div>
        <div v-else class="alert alert-warning">No profile data found.</div>
    </section>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();

onMounted(() => {
    if (!authStore.user) {
        authStore.fetchProfile();
    }
});
</script>

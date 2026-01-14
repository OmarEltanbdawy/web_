<template>
    <section>
        <h2 class="h5">Profile</h2>
        <div v-if="authStore.status === 'loading'" class="alert alert-info">Loading profile...</div>
        <div v-else-if="authStore.errorMessage" class="alert alert-danger">
            {{ authStore.errorMessage }}
        </div>
        <div v-else-if="authStore.user" class="card">
            <div class="card-body">
                <div class="d-flex align-items-center gap-3 mb-3">
                    <img
                        v-if="imagePreview || authStore.user.profileImageUrl"
                        :src="imagePreview || authStore.user.profileImageUrl || ''"
                        class="rounded-circle border"
                        style="width: 72px; height: 72px; object-fit: cover"
                        alt="Profile"
                    />
                    <div>
                        <p class="mb-1"><strong>Username:</strong> {{ authStore.user.username }}</p>
                        <p class="mb-0"><strong>Email:</strong> {{ authStore.user.email }}</p>
                    </div>
                </div>
                <form class="mt-3" @submit.prevent="submit">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label" for="username">Username</label>
                            <input id="username" v-model="form.username" class="form-control" required />
                        </div>
                        <div class="col-md-6">
                            <label class="form-label" for="email">Email</label>
                            <input id="email" v-model="form.email" class="form-control" type="email" required />
                        </div>
                        <div class="col-md-6">
                            <label class="form-label" for="dob">Date of Birth</label>
                            <input id="dob" v-model="form.dateOfBirth" class="form-control" type="date" />
                        </div>
                        <div class="col-md-6">
                            <label class="form-label" for="profileImage">Profile Image</label>
                            <input
                                id="profileImage"
                                class="form-control"
                                type="file"
                                accept="image/*"
                                @change="handleImageChange"
                            />
                        </div>
                    </div>
                    <div class="d-flex align-items-center gap-3 mt-4">
                        <button class="btn btn-primary" type="submit" :disabled="isSaving">
                            Save Changes
                        </button>
                        <span v-if="saveMessage" class="text-success">{{ saveMessage }}</span>
                    </div>
                </form>
            </div>
        </div>
        <div v-else class="alert alert-warning">No profile data found.</div>
    </section>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const imagePreview = ref<string | null>(null);
const saveMessage = ref('');
const isSaving = computed(() => authStore.status === 'loading');
const form = reactive({
    username: '',
    email: '',
    dateOfBirth: '',
    profileImage: null as File | null,
});

const hydrateForm = () => {
    if (!authStore.user) {
        return;
    }
    form.username = authStore.user.username;
    form.email = authStore.user.email;
    form.dateOfBirth = authStore.user.dateOfBirth || '';
};

const handleImageChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0] || null;
    form.profileImage = file;
    imagePreview.value = file ? URL.createObjectURL(file) : null;
};

const submit = async () => {
    if (!authStore.user) {
        return;
    }
    const payload = new FormData();
    payload.append('username', form.username);
    payload.append('email', form.email);
    if (form.dateOfBirth) {
        payload.append('date_of_birth', form.dateOfBirth);
    }
    if (form.profileImage) {
        payload.append('profile_image', form.profileImage);
    }
    const result = await authStore.saveProfile(payload);
    if (result) {
        saveMessage.value = 'Profile updated successfully.';
        setTimeout(() => {
            saveMessage.value = '';
        }, 3000);
    }
};

onMounted(() => {
    if (!authStore.user) {
        authStore.fetchProfile();
    } else {
        hydrateForm();
    }
});

watch(
    () => authStore.user,
    (profile) => {
        if (profile) {
            hydrateForm();
        }
    },
);
</script>

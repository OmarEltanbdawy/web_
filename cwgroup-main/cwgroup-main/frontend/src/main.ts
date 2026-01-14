import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { pinia } from './stores';
import { useAuthStore } from './stores/auth';
import type { AuthContext } from './types';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

type WindowWithAuth = Window & { __AUTH_CONTEXT__?: AuthContext };

const mountApp = () => {
    const app = createApp(App);
    app.use(pinia);

    const authStore = useAuthStore(pinia);
    const authContext = (window as WindowWithAuth).__AUTH_CONTEXT__;
    if (authContext) {
        authStore.bootstrap(authContext);
    } else {
        authStore.bootstrap({ isAuthenticated: false, user: null });
    }

    app.use(router);
    app.mount('#app');
};

const waitForAuth = () => {
    const windowWithAuth = window as WindowWithAuth;
    if (windowWithAuth.__AUTH_CONTEXT__) {
        mountApp();
        return;
    }

    const handleReady = () => {
        window.removeEventListener('django-auth-ready', handleReady);
        mountApp();
    };

    window.addEventListener('django-auth-ready', handleReady, { once: true });

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        mountApp();
    } else {
        document.addEventListener('DOMContentLoaded', () => {
            mountApp();
        });
    }
};

waitForAuth();

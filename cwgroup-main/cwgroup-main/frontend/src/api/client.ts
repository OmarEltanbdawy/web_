export class AuthRequiredError extends Error {
    constructor(message = 'Authentication required') {
        super(message);
        this.name = 'AuthRequiredError';
    }
}

const getCookie = (name: string): string | null => {
    const match = document.cookie.match(new RegExp(`(^|; )${name}=([^;]*)`));
    return match ? decodeURIComponent(match[2]) : null;
};

const getCsrfToken = (): string | null => getCookie('csrftoken');

export async function fetchJson<T>(input: RequestInfo | URL, init: RequestInit = {}): Promise<T> {
    const headers = new Headers(init.headers || {});
    headers.set('Accept', 'application/json');

    const method = (init.method || 'GET').toUpperCase();
    if (!['GET', 'HEAD', 'OPTIONS', 'TRACE'].includes(method)) {
        const csrfToken = getCsrfToken();
        if (csrfToken) {
            headers.set('X-CSRFToken', csrfToken);
        }
        if (!headers.has('Content-Type') && !(init.body instanceof FormData)) {
            headers.set('Content-Type', 'application/json');
        }
    }

    const response = await fetch(input, {
        credentials: 'include',
        ...init,
        headers,
    });

    if (response.status === 401) {
        throw new AuthRequiredError();
    }

    if (!response.ok) {
        const message = await response.text();
        throw new Error(message || `Request failed with status ${response.status}`);
    }

    if (response.status === 204) {
        return undefined as T;
    }

    return (await response.json()) as T;
}

export class ApiClient {
    constructor(baseUrl = "") {
        this.baseUrl = baseUrl;
    }

    async request(path, options = {}) {
        const response = await fetch(`${this.baseUrl}${path}`, {
            ...options,
            headers: {
                "Accept": "application/json",
                ...options.headers,
            },
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}`);
        }

        const contentType = response.headers.get("content-type") || "";
        return contentType.includes("application/json")
            ? response.json()
            : response.text();
    }

    get(path, options = {}) {
        return this.request(path, { ...options, method: "GET" });
    }

    post(path, data = {}, options = {}) {
        return this.request(path, {
            ...options,
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
            body: JSON.stringify(data),
        });
    }
}

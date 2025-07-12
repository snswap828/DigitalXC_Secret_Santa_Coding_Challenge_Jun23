import axios from 'axios';

const apiUrl = process.env.NEXT_PUBLIC_API_URL;


const createApiClient = (env: 'client' | 'server') => {
  const api = axios.create({
    baseURL: `${apiUrl}/api/`,
  });
  // Add a method to get URL parameters

  api.interceptors.request.use(
    async config => {
      let token;

      if (env === 'client') {
        // For client-side requests
        token = localStorage.getItem('accessToken');
      } else {
        // For server-side requests
      }

      if (token) {
        config.headers['X-Access-Token'] = token;
      }

      return config;
    },
    error => Promise.reject(error),
  );

  api.interceptors.response.use(
    response => response,
    async error => {
      const originalRequest = error.config;

      if (
        error.response &&
        error.response.status === 401 &&
        !originalRequest._retry
      ) {
        originalRequest._retry = true;
        console.error('Access token expired or invalid');
        try {
            return api(originalRequest);
          // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (refreshError) {
          console.error('Refresh token expired or invalid');

          // Clear login logic if needed
        }
      }

      return Promise.reject(error);
    },
  );

  return api;
};

const apiClient = createApiClient('client');
const apiServer = createApiClient('server');

export { apiClient, apiServer };

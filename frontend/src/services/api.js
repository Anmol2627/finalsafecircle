const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const api = {
  // User endpoints
  getUsers: async () => {
    const response = await fetch(`${API_URL}/users`);
    if (!response.ok) throw new Error('Failed to fetch users');
    return response.json();
  },

  getUser: async (id) => {
    const response = await fetch(`${API_URL}/users/${id}`);
    if (!response.ok) throw new Error('Failed to fetch user');
    return response.json();
  },

  login: async (email, password) => {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) {
      if (response.status === 401) throw new Error('Invalid credentials');
      throw new Error('Login failed');
    }
    return response.json();
  },

  createUser: async (userData) => {
    const response = await fetch(`${API_URL}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    if (!response.ok) throw new Error('Failed to create user');
    return response.json();
  },

  updateUser: async (id, updates) => {
    const response = await fetch(`${API_URL}/users/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    if (!response.ok) throw new Error('Failed to update user');
    return response.json();
  },

  updateLocation: async (userId, location) => {
    const response = await fetch(`${API_URL}/users/${userId}/location`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(location),
    });
    if (!response.ok) throw new Error('Failed to update location');
    return response.json();
  },

  // Incident endpoints
  getIncidents: async () => {
    const response = await fetch(`${API_URL}/incidents`);
    if (!response.ok) throw new Error('Failed to fetch incidents');
    return response.json();
  },

  createIncident: async (incidentData) => {
    const response = await fetch(`${API_URL}/incidents`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(incidentData),
    });
    if (!response.ok) throw new Error('Failed to create incident');
    return response.json();
  },

  getIncident: async (id) => {
    const response = await fetch(`${API_URL}/incidents/${id}`);
    if (!response.ok) throw new Error('Failed to fetch incident');
    return response.json();
  },

  // Leaderboard
  getLeaderboard: async () => {
    const response = await fetch(`${API_URL}/leaderboard`);
    if (!response.ok) throw new Error('Failed to fetch leaderboard');
    return response.json();
  }
};

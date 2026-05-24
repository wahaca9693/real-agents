/**
 * Real Agents - API Service
 * خدمة API للاتصال بالخادم
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('auth_token');
  }

  // ============================================
  // HTTP Methods
  // ============================================

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    // Add auth token if available
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      // Handle 401 Unauthorized
      if (response.status === 401) {
        // Try to refresh token
        const refreshed = await this.refreshToken();
        if (refreshed) {
          // Retry the request
          headers['Authorization'] = `Bearer ${this.token}`;
          const retryResponse = await fetch(url, { ...options, headers });
          return this.handleResponse(retryResponse);
        }
        // Logout user
        this.logout();
        throw new Error('Session expired');
      }

      return this.handleResponse(response);
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async handleResponse(response) {
    const data = await response.json();
    
    if (!response.ok) {
      const error = new Error(data.detail || 'An error occurred');
      error.status = response.status;
      error.data = data;
      throw error;
    }
    
    return data;
  }

  // ============================================
  // Auth Methods
  // ============================================

  async register(name, email, password, phone = null) {
    const response = await this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password, phone }),
    });
    
    if (response.access_token) {
      this.setToken(response.access_token);
    }
    
    return response;
  }

  async login(email, password) {
    const response = await this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    if (response.access_token) {
      this.setToken(response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
    }
    
    return response;
  }

  async verifyEmail(email, code) {
    const response = await this.request('/api/auth/verify-email', {
      method: 'POST',
      body: JSON.stringify({ email, code }),
    });
    
    if (response.access_token) {
      this.setToken(response.access_token);
    }
    
    return response;
  }

  async refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return false;

    try {
      const response = await this.request('/api/auth/refresh-token', {
        method: 'POST',
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (response.access_token) {
        this.setToken(response.access_token);
        localStorage.setItem('refresh_token', response.refresh_token);
        return true;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }
    
    return false;
  }

  async logout() {
    try {
      await this.request('/api/auth/logout', { method: 'POST' });
    } catch (e) {
      // Ignore errors on logout
    }
    this.clearTokens();
  }

  async getProfile() {
    return this.request('/api/auth/me');
  }

  async updateProfile(data) {
    return this.request('/api/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async changePassword(oldPassword, newPassword) {
    return this.request('/api/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
    });
  }

  // ============================================
  // Agents Methods
  // ============================================

  async getAgents() {
    return this.request('/api/agents');
  }

  async getAgent(agentId) {
    return this.request(`/api/agents/${agentId}`);
  }

  async agentThink(agentId, message) {
    return this.request(`/api/agents/${agentId}/think`, {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  async agentTask(agentId, task) {
    return this.request(`/api/agents/${agentId}/task`, {
      method: 'POST',
      body: JSON.stringify({ task }),
    });
  }

  // ============================================
  // Chat Methods
  // ============================================

  async sendChatMessage(message) {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  async coordinateTask(task) {
    return this.request('/api/coordinate', {
      method: 'POST',
      body: JSON.stringify({ task }),
    });
  }

  // ============================================
  // VSCode Methods
  // ============================================

  async createProject(name, type) {
    return this.request('/api/vscode/project', {
      method: 'POST',
      body: JSON.stringify({ name, type }),
    });
  }

  async createFile(projectName, path, content) {
    return this.request('/api/vscode/file', {
      method: 'POST',
      body: JSON.stringify({ project_name: projectName, path, content }),
    });
  }

  // ============================================
  // Shell Methods
  // ============================================

  async executeCommand(command, timeout = 60) {
    return this.request('/api/shell', {
      method: 'POST',
      body: JSON.stringify({ command, timeout }),
    });
  }

  async runGitCommand(command, repoPath = null) {
    return this.request('/api/shell/git', {
      method: 'POST',
      body: JSON.stringify({ command, repo_path: repoPath }),
    });
  }

  async runNpmCommand(command, projectPath = null) {
    return this.request('/api/shell/npm', {
      method: 'POST',
      body: JSON.stringify({ command, project_path: projectPath }),
    });
  }

  async runDockerCommand(command) {
    return this.request('/api/shell/docker', {
      method: 'POST',
      body: JSON.stringify({ command }),
    });
  }

  // ============================================
  // Team Methods
  // ============================================

  async getTeam() {
    return this.request('/team/team');
  }

  async getTeamList() {
    return this.request('/team/list');
  }

  async getTeamStats() {
    return this.request('/team/stats');
  }

  async getLeaderboard() {
    return this.request('/team/leaderboard');
  }

  async createTask(title, description, taskType = 'development') {
    return this.request('/team/tasks/create', {
      method: 'POST',
      body: JSON.stringify({ title, description, task_type: taskType }),
    });
  }

  async getTasks() {
    return this.request('/team/tasks/list');
  }

  // ============================================
  // System Methods
  // ============================================

  async getSystemInfo() {
    return this.request('/api/system/info');
  }

  async getCommandHistory() {
    return this.request('/api/system/history');
  }

  async healthCheck() {
    return this.request('/api/health');
  }

  // ============================================
  // Token Management
  // ============================================

  setToken(token) {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  clearTokens() {
    this.token = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }

  isAuthenticated() {
    return !!this.token;
  }
}

// Export singleton instance
export const api = new ApiService();
export default api;
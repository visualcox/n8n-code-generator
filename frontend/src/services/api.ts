/**
 * API Service for n8n JSON Generator
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface UserRequirement {
  requirement: string;
  context?: string;
}

export interface Answer {
  question_id: string;
  answer: string;
}

export interface WorkflowRequest {
  id: number;
  status: string;
  user_requirement: string;
  analyzed_requirement?: any;
  questions_asked?: any[];
  development_spec?: string;
  generated_json?: string;
  test_results?: any;
  final_json?: string;
  created_at: string;
  updated_at: string;
}

export interface LLMConfig {
  id?: number;
  name: string;
  provider: string;
  api_key?: string;
  api_url?: string;
  model_name: string;
  temperature: number;
  max_tokens: number;
  is_default: boolean;
}

// Workflow API
export const workflowApi = {
  create: async (requirement: UserRequirement): Promise<WorkflowRequest> => {
    const response = await apiClient.post('/api/workflow/create', requirement);
    return response.data;
  },

  analyze: async (requestId: number): Promise<any> => {
    const response = await apiClient.post(`/api/workflow/${requestId}/analyze`);
    return response.data;
  },

  submitAnswers: async (requestId: number, answers: Answer[]): Promise<any> => {
    const response = await apiClient.post(`/api/workflow/${requestId}/answers`, answers);
    return response.data;
  },

  generateSpec: async (requestId: number): Promise<{ development_spec: string }> => {
    const response = await apiClient.post(`/api/workflow/${requestId}/generate-spec`);
    return response.data;
  },

  updateSpec: async (requestId: number, spec: string): Promise<any> => {
    const response = await apiClient.put(`/api/workflow/${requestId}/update-spec`, {
      development_spec: spec,
    });
    return response.data;
  },

  generateJson: async (requestId: number): Promise<{ workflow_json: string }> => {
    const response = await apiClient.post(`/api/workflow/${requestId}/generate-json`);
    return response.data;
  },

  testAndOptimize: async (requestId: number): Promise<any> => {
    const response = await apiClient.post(`/api/workflow/${requestId}/test-optimize`);
    return response.data;
  },

  get: async (requestId: number): Promise<WorkflowRequest> => {
    const response = await apiClient.get(`/api/workflow/${requestId}`);
    return response.data;
  },

  list: async (skip = 0, limit = 20): Promise<{ total: number; items: WorkflowRequest[] }> => {
    const response = await apiClient.get('/api/workflow/', { params: { skip, limit } });
    return response.data;
  },
};

// LLM Config API
export const llmConfigApi = {
  create: async (config: LLMConfig): Promise<LLMConfig> => {
    const response = await apiClient.post('/api/llm/config', config);
    return response.data;
  },

  list: async (): Promise<LLMConfig[]> => {
    const response = await apiClient.get('/api/llm/config');
    return response.data;
  },

  get: async (configId: number): Promise<LLMConfig> => {
    const response = await apiClient.get(`/api/llm/config/${configId}`);
    return response.data;
  },

  activate: async (configId: number): Promise<any> => {
    const response = await apiClient.put(`/api/llm/config/${configId}/activate`);
    return response.data;
  },

  delete: async (configId: number): Promise<any> => {
    const response = await apiClient.delete(`/api/llm/config/${configId}`);
    return response.data;
  },
};

// Learning API
export const learningApi = {
  runCycle: async (): Promise<any> => {
    const response = await apiClient.post('/api/learning/run');
    return response.data;
  },

  listExamples: async (skip = 0, limit = 50, source?: string): Promise<any[]> => {
    const response = await apiClient.get('/api/learning/examples', {
      params: { skip, limit, source },
    });
    return response.data;
  },

  getExample: async (exampleId: number): Promise<any> => {
    const response = await apiClient.get(`/api/learning/examples/${exampleId}`);
    return response.data;
  },

  getLogs: async (skip = 0, limit = 20): Promise<any[]> => {
    const response = await apiClient.get('/api/learning/logs', { params: { skip, limit } });
    return response.data;
  },

  getStats: async (): Promise<any> => {
    const response = await apiClient.get('/api/learning/stats');
    return response.data;
  },
};

export default apiClient;

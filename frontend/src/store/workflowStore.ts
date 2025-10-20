/**
 * Zustand store for workflow state management
 */
import { create } from 'zustand';
import { WorkflowRequest } from '../services/api';

interface WorkflowState {
  currentWorkflow: WorkflowRequest | null;
  workflows: WorkflowRequest[];
  loading: boolean;
  error: string | null;
  
  setCurrentWorkflow: (workflow: WorkflowRequest | null) => void;
  setWorkflows: (workflows: WorkflowRequest[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  updateCurrentWorkflow: (updates: Partial<WorkflowRequest>) => void;
}

export const useWorkflowStore = create<WorkflowState>((set) => ({
  currentWorkflow: null,
  workflows: [],
  loading: false,
  error: null,

  setCurrentWorkflow: (workflow) => set({ currentWorkflow: workflow }),
  
  setWorkflows: (workflows) => set({ workflows }),
  
  setLoading: (loading) => set({ loading }),
  
  setError: (error) => set({ error }),
  
  updateCurrentWorkflow: (updates) =>
    set((state) => ({
      currentWorkflow: state.currentWorkflow
        ? { ...state.currentWorkflow, ...updates }
        : null,
    })),
}));

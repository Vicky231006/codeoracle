/**
 * API endpoint functions for CodeOracle
 */
import apiClient from './client';
import type {
  HealthResponse,
  SystemStatusResponse,
  RepositoryAnalysisRequest,
  RepositoryAnalysisResponse,
  DependencyAnalysisRequest,
  DependencyAnalysisResponse,
  RiskAssessmentRequest,
  RiskAssessmentResponse,
  QueryRequest,
  QueryResponse,
  ImpactSimulationRequest,
  ImpactSimulationResponse,
  OrchestrationRequest,
  OrchestrationResponse,
} from './types';

/**
 * Health check endpoint
 */
export const checkHealth = async (): Promise<HealthResponse> => {
  const response = await apiClient.get<HealthResponse>('/api/health');
  return response.data;
};

/**
 * Get system status
 */
export const getSystemStatus = async (): Promise<SystemStatusResponse> => {
  const response = await apiClient.get<SystemStatusResponse>('/api/status');
  return response.data;
};

/**
 * Analyze repository
 */
export const analyzeRepository = async (
  request: RepositoryAnalysisRequest
): Promise<RepositoryAnalysisResponse> => {
  const response = await apiClient.post<RepositoryAnalysisResponse>(
    '/api/analyze/repository',
    request
  );
  return response.data;
};

/**
 * Analyze dependencies
 */
export const analyzeDependencies = async (
  request: DependencyAnalysisRequest
): Promise<DependencyAnalysisResponse> => {
  const response = await apiClient.post<DependencyAnalysisResponse>(
    '/api/analyze/dependencies',
    request
  );
  return response.data;
};

/**
 * Assess risks
 */
export const assessRisks = async (
  request: RiskAssessmentRequest
): Promise<RiskAssessmentResponse> => {
  const response = await apiClient.post<RiskAssessmentResponse>(
    '/api/analyze/risk',
    request
  );
  return response.data;
};

/**
 * Query codebase
 */
export const queryCodebase = async (
  request: QueryRequest
): Promise<QueryResponse> => {
  const response = await apiClient.post<QueryResponse>(
    '/api/query',
    request
  );
  return response.data;
};

/**
 * Simulate impact
 */
export const simulateImpact = async (
  request: ImpactSimulationRequest
): Promise<ImpactSimulationResponse> => {
  const response = await apiClient.post<ImpactSimulationResponse>(
    '/api/simulate/impact',
    request
  );
  return response.data;
};

/**
 * Orchestrate task
 */
export const orchestrateTask = async (
  request: OrchestrationRequest
): Promise<OrchestrationResponse> => {
  const response = await apiClient.post<OrchestrationResponse>(
    '/api/orchestrate',
    request
  );
  return response.data;
};

/**
 * Clear cache
 */
export const clearCache = async (): Promise<{ status: string; message: string }> => {
  const response = await apiClient.delete<{ status: string; message: string }>(
    '/api/cache'
  );
  return response.data;
};

/**
 * Upload manifest file (mock implementation - adjust based on actual backend)
 */
export const uploadManifest = async (file: File): Promise<{ path: string }> => {
  const formData = new FormData();
  formData.append('file', file);
  
  // This is a placeholder - adjust based on actual upload endpoint
  const response = await apiClient.post<{ path: string }>(
    '/api/upload/manifest',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );
  return response.data;
};

// Export all endpoints as a single object
export const api = {
  checkHealth,
  getSystemStatus,
  analyzeRepository,
  analyzeDependencies,
  assessRisks,
  queryCodebase,
  simulateImpact,
  orchestrateTask,
  clearCache,
  uploadManifest,
};

export default api;

// Made with Bob

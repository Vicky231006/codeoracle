/**
 * TypeScript types for CodeOracle API
 */

// Agent Types
export type AgentType = 
  | 'repo_mapper'
  | 'dependency_analyst'
  | 'risk_detector'
  | 'knowledge_synthesizer'
  | 'impact_simulator';

export type AnalysisDepth = 'quick' | 'standard' | 'deep';
export type ChangeType = 'addition' | 'modification' | 'deletion';
export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

// Health & Status
export interface HealthResponse {
  status: string;
  version: string;
  agents_available: string[];
}

export interface AgentStatus {
  name: string;
  type: string;
  status: string;
  last_execution?: number;
}

export interface SystemStatusResponse {
  status: string;
  agents: AgentStatus[];
  cache_size: number;
  uptime: number;
}

// Error Response
export interface ErrorResponse {
  error: string;
  detail?: string;
  code?: string;
}

// Repository Analysis
export interface RepositoryAnalysisRequest {
  manifest_path: string;
  manifest?: Record<string, any>;
  analysis_depth?: AnalysisDepth;
}

export interface RepositoryAnalysisResponse {
  status: string;
  repository_map: Record<string, any>;
  dependencies: Record<string, any>;
  risks: Record<string, any>;
  summary: string;
  execution_time: number;
}

// Dependency Analysis
export interface DependencyAnalysisRequest {
  manifest_path: string;
  manifest?: Record<string, any>;
  focus_areas?: string[];
}

export interface DependencyAnalysisResponse {
  status: string;
  dependencies: Record<string, any>;
  vulnerabilities: Array<Record<string, any>>;
  recommendations: string[];
  execution_time: number;
}

// Risk Assessment
export interface RiskAssessmentRequest {
  manifest_path: string;
  manifest?: Record<string, any>;
  risk_categories?: string[];
}

export interface RiskAssessmentResponse {
  status: string;
  risks: Array<Record<string, any>>;
  overall_risk_score: number;
  critical_issues: Array<Record<string, any>>;
  recommendations: string[];
  execution_time: number;
}

// Query
export interface QueryRequest {
  manifest_path: string;
  manifest?: Record<string, any>;
  query: string;
  context?: Record<string, any>;
}

export interface QueryResponse {
  status: string;
  answer: string;
  sources: Array<Record<string, any>>;
  confidence: number;
  execution_time: number;
}

// Impact Simulation
export interface ImpactSimulationRequest {
  manifest_path: string;
  manifest?: Record<string, any>;
  change_description: string;
  affected_files?: string[];
  change_type?: ChangeType;
}

export interface ImpactSimulationResponse {
  status: string;
  impact_analysis: Record<string, any>;
  affected_components: Array<Record<string, any>>;
  risk_level: RiskLevel;
  recommendations: string[];
  test_suggestions: string[];
  execution_time: number;
}

// Orchestration
export interface OrchestrationRequest {
  manifest_path: string;
  manifest?: Record<string, any>;
  task: string;
  agents_to_use?: AgentType[];
  max_iterations?: number;
}

export interface OrchestrationResponse {
  status: string;
  task_result: Record<string, any>;
  agents_used: string[];
  execution_plan: Array<Record<string, any>>;
  total_execution_time: number;
  recommendations: string[];
}

// UI-specific types
export interface UploadedManifest {
  path: string;
  name: string;
  size: number;
  uploadedAt: Date;
  content?: Record<string, any>;
}

export interface AnalysisState {
  isLoading: boolean;
  error: string | null;
  data: RepositoryAnalysisResponse | null;
}

export interface DependencyNode {
  id: string;
  name: string;
  type: string;
  dependencies: string[];
  dependents: string[];
}

export interface RiskItem {
  id: string;
  severity: RiskLevel;
  category: string;
  description: string;
  location: string;
  recommendation: string;
}

export interface ComponentInfo {
  name: string;
  type: string;
  path: string;
  lines_of_code: number;
  complexity?: number;
  dependencies: string[];
}

// Made with Bob

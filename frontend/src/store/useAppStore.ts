/**
 * Global application state management using Zustand
 */
import { create } from 'zustand';
import type {
  RepositoryAnalysisResponse,
  DependencyAnalysisResponse,
  RiskAssessmentResponse,
  QueryResponse,
  ImpactSimulationResponse,
  UploadedManifest,
} from '../api/types';

interface AppState {
  // Manifest
  currentManifest: UploadedManifest | null;
  setCurrentManifest: (manifest: UploadedManifest | null) => void;

  // Analysis results
  repositoryAnalysis: RepositoryAnalysisResponse | null;
  dependencyAnalysis: DependencyAnalysisResponse | null;
  riskAssessment: RiskAssessmentResponse | null;
  
  setRepositoryAnalysis: (analysis: RepositoryAnalysisResponse | null) => void;
  setDependencyAnalysis: (analysis: DependencyAnalysisResponse | null) => void;
  setRiskAssessment: (assessment: RiskAssessmentResponse | null) => void;

  // Query history
  queryHistory: QueryResponse[];
  addQueryToHistory: (query: QueryResponse) => void;
  clearQueryHistory: () => void;

  // Impact simulations
  impactSimulations: ImpactSimulationResponse[];
  addImpactSimulation: (simulation: ImpactSimulationResponse) => void;
  clearImpactSimulations: () => void;

  // Loading states
  isAnalyzing: boolean;
  setIsAnalyzing: (isAnalyzing: boolean) => void;

  // Error handling
  error: string | null;
  setError: (error: string | null) => void;

  // Dark mode
  isDarkMode: boolean;
  toggleDarkMode: () => void;

  // Reset all state
  resetState: () => void;
}

const initialState = {
  currentManifest: null,
  repositoryAnalysis: null,
  dependencyAnalysis: null,
  riskAssessment: null,
  queryHistory: [],
  impactSimulations: [],
  isAnalyzing: false,
  error: null,
  isDarkMode: localStorage.getItem('darkMode') === 'true',
};

export const useAppStore = create<AppState>((set) => ({
  ...initialState,

  setCurrentManifest: (manifest) => set({ currentManifest: manifest }),

  setRepositoryAnalysis: (analysis) => set({ repositoryAnalysis: analysis }),
  setDependencyAnalysis: (analysis) => set({ dependencyAnalysis: analysis }),
  setRiskAssessment: (assessment) => set({ riskAssessment: assessment }),

  addQueryToHistory: (query) =>
    set((state) => ({
      queryHistory: [query, ...state.queryHistory].slice(0, 50), // Keep last 50 queries
    })),

  clearQueryHistory: () => set({ queryHistory: [] }),

  addImpactSimulation: (simulation) =>
    set((state) => ({
      impactSimulations: [simulation, ...state.impactSimulations].slice(0, 20), // Keep last 20
    })),

  clearImpactSimulations: () => set({ impactSimulations: [] }),

  setIsAnalyzing: (isAnalyzing) => set({ isAnalyzing }),

  setError: (error) => set({ error }),

  toggleDarkMode: () =>
    set((state) => {
      const newDarkMode = !state.isDarkMode;
      localStorage.setItem('darkMode', String(newDarkMode));
      if (newDarkMode) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      return { isDarkMode: newDarkMode };
    }),

  resetState: () => set(initialState),
}));

// Initialize dark mode on load
if (localStorage.getItem('darkMode') === 'true') {
  document.documentElement.classList.add('dark');
}

// Made with Bob

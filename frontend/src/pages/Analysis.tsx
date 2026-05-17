/**
 * Analysis page component
 */
import React, { useState } from 'react';
import { Play, RefreshCw } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';
import RepositoryUpload from '../components/RepositoryUpload';
import AnalysisDashboard from '../components/AnalysisDashboard';
import LoadingSpinner from '../components/LoadingSpinner';
import { analyzeRepository } from '../api/endpoints';
import toast from 'react-hot-toast';

const Analysis: React.FC = () => {
  const {
    currentManifest,
    setRepositoryAnalysis,
    setDependencyAnalysis,
    setRiskAssessment,
    isAnalyzing,
    setIsAnalyzing,
    setError,
  } = useAppStore();

  const [analysisDepth, setAnalysisDepth] = useState<'quick' | 'standard' | 'deep'>('standard');

  const handleAnalyze = async () => {
    if (!currentManifest) {
      toast.error('Please upload a manifest file first');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      const payload: any = {
        manifest_path: currentManifest.path,
        analysis_depth: analysisDepth,
      };
      if (currentManifest.content) {
        payload.manifest = currentManifest.content;
      }
      const result = await analyzeRepository(payload);

      setRepositoryAnalysis(result);
      
      // Extract dependency and risk data if available
      if (result.dependencies) {
        setDependencyAnalysis({
          status: 'success',
          dependencies: result.dependencies,
          vulnerabilities: [],
          recommendations: [],
          execution_time: result.execution_time,
        });
      }

      if (result.risks) {
        setRiskAssessment({
          status: 'success',
          risks: [],
          overall_risk_score: 0,
          critical_issues: [],
          recommendations: [],
          execution_time: result.execution_time,
        });
      }

      toast.success('Analysis completed successfully!');
    } catch (error: any) {
      const errorMessage = error?.error || error?.message || 'Analysis failed';
      setError(errorMessage);
      toast.error(errorMessage);
      console.error('Analysis error:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setRepositoryAnalysis(null);
    setDependencyAnalysis(null);
    setRiskAssessment(null);
    setError(null);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Repository Analysis
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Upload your repository manifest and get comprehensive insights
        </p>
      </div>

      {/* Upload Section */}
      {!currentManifest && (
        <div className="card">
          <RepositoryUpload />
        </div>
      )}

      {/* Analysis Controls */}
      {currentManifest && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                Current Manifest
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                {currentManifest.name}
              </p>
            </div>
            <button
              onClick={handleReset}
              className="btn-secondary inline-flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Change Manifest
            </button>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Analysis Depth
              </label>
              <div className="flex gap-3">
                {(['quick', 'standard', 'deep'] as const).map((depth) => (
                  <button
                    key={depth}
                    onClick={() => setAnalysisDepth(depth)}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                      analysisDepth === depth
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600'
                    }`}
                  >
                    {depth.charAt(0).toUpperCase() + depth.slice(1)}
                  </button>
                ))}
              </div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                {analysisDepth === 'quick' && 'Fast analysis with basic insights'}
                {analysisDepth === 'standard' && 'Balanced analysis with detailed insights'}
                {analysisDepth === 'deep' && 'Comprehensive analysis with maximum detail'}
              </p>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className="btn-primary w-full inline-flex items-center justify-center gap-2 text-lg py-3"
            >
              {isAnalyzing ? (
                <>
                  <LoadingSpinner size="sm" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Play className="w-5 h-5" />
                  Run Analysis
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Results Dashboard */}
      {currentManifest && (
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Analysis Results
          </h2>
          <AnalysisDashboard />
        </div>
      )}
    </div>
  );
};

export default Analysis;

// Made with Bob

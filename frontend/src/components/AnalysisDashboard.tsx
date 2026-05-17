/**
 * Main analysis dashboard component
 */
import React from 'react';
import { 
  Activity, 
  GitBranch, 
  AlertTriangle, 
  Clock,
  CheckCircle,
  XCircle
} from 'lucide-react';
import { useAppStore } from '../store/useAppStore';
import LoadingSpinner from './LoadingSpinner';

export const AnalysisDashboard: React.FC = () => {
  const { 
    repositoryAnalysis, 
    dependencyAnalysis, 
    riskAssessment,
    isAnalyzing 
  } = useAppStore();

  if (isAnalyzing) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" text="Analyzing repository..." />
      </div>
    );
  }

  if (!repositoryAnalysis && !dependencyAnalysis && !riskAssessment) {
    return (
      <div className="text-center py-12">
        <Activity className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          No Analysis Data
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Upload a repository manifest and run an analysis to see results here.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Repository Status */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Repository
            </h3>
            <Activity className="w-5 h-5 text-primary-600 dark:text-primary-400" />
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {repositoryAnalysis ? 'Analyzed' : 'Pending'}
          </p>
          {repositoryAnalysis && (
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {repositoryAnalysis.execution_time.toFixed(2)}s
            </p>
          )}
        </div>

        {/* Dependencies */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Dependencies
            </h3>
            <GitBranch className="w-5 h-5 text-secondary-600 dark:text-secondary-400" />
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {dependencyAnalysis?.vulnerabilities?.length || 0}
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Vulnerabilities
          </p>
        </div>

        {/* Risk Score */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Risk Score
            </h3>
            <AlertTriangle className="w-5 h-5 text-warning-600 dark:text-warning-400" />
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {riskAssessment?.overall_risk_score?.toFixed(1) || 'N/A'}
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Out of 100
          </p>
        </div>

        {/* Critical Issues */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Critical Issues
            </h3>
            <XCircle className="w-5 h-5 text-danger-600 dark:text-danger-400" />
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {riskAssessment?.critical_issues?.length || 0}
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Require attention
          </p>
        </div>
      </div>

      {/* Repository Analysis */}
      {repositoryAnalysis && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <Activity className="w-6 h-6 text-primary-600 dark:text-primary-400" />
            Repository Analysis
          </h2>
          <div className="prose dark:prose-invert max-w-none">
            <p className="text-gray-700 dark:text-gray-300">
              {repositoryAnalysis.summary}
            </p>
          </div>
          <div className="mt-4 flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
            <Clock className="w-4 h-4" />
            <span>Completed in {repositoryAnalysis.execution_time.toFixed(2)}s</span>
          </div>
        </div>
      )}

      {/* Dependency Analysis */}
      {dependencyAnalysis && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <GitBranch className="w-6 h-6 text-secondary-600 dark:text-secondary-400" />
            Dependency Analysis
          </h2>
          
          {dependencyAnalysis.vulnerabilities.length > 0 ? (
            <div className="space-y-3">
              {dependencyAnalysis.vulnerabilities.slice(0, 5).map((vuln, idx) => (
                <div 
                  key={idx}
                  className="p-4 bg-warning-50 dark:bg-warning-900/20 border border-warning-200 dark:border-warning-800 rounded-lg"
                >
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="w-5 h-5 text-warning-600 dark:text-warning-400 flex-shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 dark:text-white">
                        {vuln.name || 'Vulnerability'}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {vuln.description || 'No description available'}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
              {dependencyAnalysis.vulnerabilities.length > 5 && (
                <p className="text-sm text-gray-500 dark:text-gray-400 text-center">
                  And {dependencyAnalysis.vulnerabilities.length - 5} more...
                </p>
              )}
            </div>
          ) : (
            <div className="flex items-center gap-2 text-success-600 dark:text-success-400">
              <CheckCircle className="w-5 h-5" />
              <span>No vulnerabilities detected</span>
            </div>
          )}

          {dependencyAnalysis.recommendations.length > 0 && (
            <div className="mt-4">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                Recommendations
              </h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                {dependencyAnalysis.recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Risk Assessment */}
      {riskAssessment && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <AlertTriangle className="w-6 h-6 text-warning-600 dark:text-warning-400" />
            Risk Assessment
          </h2>

          {riskAssessment.critical_issues.length > 0 && (
            <div className="mb-6">
              <h3 className="font-semibold text-danger-600 dark:text-danger-400 mb-3">
                Critical Issues
              </h3>
              <div className="space-y-3">
                {riskAssessment.critical_issues.map((issue, idx) => (
                  <div 
                    key={idx}
                    className="p-4 bg-danger-50 dark:bg-danger-900/20 border border-danger-200 dark:border-danger-800 rounded-lg"
                  >
                    <p className="font-medium text-gray-900 dark:text-white">
                      {issue.title || 'Critical Issue'}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {issue.description || 'No description available'}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {riskAssessment.recommendations.length > 0 && (
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                Recommendations
              </h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                {riskAssessment.recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AnalysisDashboard;

// Made with Bob

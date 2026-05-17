/**
 * Impact simulation page
 */
import React, { useState } from 'react';
import { Zap, AlertTriangle } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';
import { simulateImpact } from '../api/endpoints';
import LoadingSpinner from '../components/LoadingSpinner';
import toast from 'react-hot-toast';

const Impact: React.FC = () => {
  const { currentManifest, impactSimulations, addImpactSimulation } = useAppStore();
  const [changeDescription, setChangeDescription] = useState('');
  const [affectedFiles, setAffectedFiles] = useState('');
  const [changeType, setChangeType] = useState<'addition' | 'modification' | 'deletion'>('modification');
  const [isSimulating, setIsSimulating] = useState(false);
  const [currentResult, setCurrentResult] = useState<any>(null);

  const handleSimulate = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!currentManifest) {
      toast.error('Please upload a manifest file first');
      return;
    }

    if (!changeDescription.trim()) {
      toast.error('Please describe the change');
      return;
    }

    setIsSimulating(true);
    setCurrentResult(null);

    try {
      const files = affectedFiles
        .split('\n')
        .map(f => f.trim())
        .filter(f => f.length > 0);

      const result = await simulateImpact({
        manifest_path: currentManifest.path,
        manifest: currentManifest.content,
        change_description: changeDescription.trim(),
        affected_files: files.length > 0 ? files : undefined,
        change_type: changeType,
      });

      setCurrentResult(result);
      addImpactSimulation(result);
      toast.success('Impact simulation completed!');
    } catch (error: any) {
      toast.error(error?.error || 'Simulation failed');
      console.error('Simulation error:', error);
    } finally {
      setIsSimulating(false);
    }
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-success-600 dark:text-success-400 bg-success-50 dark:bg-success-900/20';
      case 'medium': return 'text-warning-600 dark:text-warning-400 bg-warning-50 dark:bg-warning-900/20';
      case 'high': return 'text-danger-600 dark:text-danger-400 bg-danger-50 dark:bg-danger-900/20';
      case 'critical': return 'text-danger-700 dark:text-danger-300 bg-danger-100 dark:bg-danger-900/30';
      default: return 'text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-900/20';
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Impact Simulation
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Predict the impact of code changes before implementation
        </p>
      </div>

      {!currentManifest ? (
        <div className="card text-center">
          <Zap className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            No Manifest Loaded
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Please upload a repository manifest in the Analysis page first.
          </p>
        </div>
      ) : (
        <>
          {/* Simulation Form */}
          <div className="card">
            <form onSubmit={handleSimulate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Change Description
                </label>
                <textarea
                  value={changeDescription}
                  onChange={(e) => setChangeDescription(e.target.value)}
                  placeholder="Describe the change you want to make..."
                  rows={4}
                  className="input w-full resize-none"
                  disabled={isSimulating}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Affected Files (one per line, optional)
                </label>
                <textarea
                  value={affectedFiles}
                  onChange={(e) => setAffectedFiles(e.target.value)}
                  placeholder="src/main.py&#10;src/utils.py"
                  rows={3}
                  className="input w-full resize-none font-mono text-sm"
                  disabled={isSimulating}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Change Type
                </label>
                <div className="flex gap-3">
                  {(['addition', 'modification', 'deletion'] as const).map((type) => (
                    <button
                      key={type}
                      type="button"
                      onClick={() => setChangeType(type)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        changeType === type
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600'
                      }`}
                    >
                      {type.charAt(0).toUpperCase() + type.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              <button
                type="submit"
                disabled={isSimulating || !changeDescription.trim()}
                className="btn-primary w-full inline-flex items-center justify-center gap-2"
              >
                {isSimulating ? (
                  <>
                    <LoadingSpinner size="sm" />
                    Simulating...
                  </>
                ) : (
                  <>
                    <Zap className="w-5 h-5" />
                    Simulate Impact
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Current Result */}
          {currentResult && (
            <div className="card">
              <div className="flex items-center gap-3 mb-4">
                <AlertTriangle className="w-6 h-6 text-warning-600 dark:text-warning-400" />
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  Impact Analysis
                </h2>
              </div>

              <div className="space-y-4">
                <div className={`px-4 py-3 rounded-lg ${getRiskColor(currentResult.risk_level)}`}>
                  <p className="font-semibold">
                    Risk Level: {currentResult.risk_level.toUpperCase()}
                  </p>
                </div>

                {currentResult.affected_components.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                      Affected Components ({currentResult.affected_components.length})
                    </h3>
                    <div className="space-y-2">
                      {currentResult.affected_components.map((comp: any, idx: number) => (
                        <div key={idx} className="p-3 bg-gray-50 dark:bg-gray-700 rounded">
                          <p className="font-medium text-gray-900 dark:text-white">
                            {comp.name || comp.component || `Component ${idx + 1}`}
                          </p>
                          {comp.impact && (
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                              {comp.impact}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {currentResult.recommendations.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                      Recommendations
                    </h3>
                    <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                      {currentResult.recommendations.map((rec: string, idx: number) => (
                        <li key={idx}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {currentResult.test_suggestions.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                      Suggested Tests
                    </h3>
                    <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                      {currentResult.test_suggestions.map((test: string, idx: number) => (
                        <li key={idx}>{test}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Simulation History */}
          {impactSimulations.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Recent Simulations
              </h3>
              <div className="space-y-3">
                {impactSimulations.slice(0, 5).map((sim, idx) => (
                  <div key={idx} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className={`px-2 py-1 rounded text-sm font-medium ${getRiskColor(sim.risk_level)}`}>
                        {sim.risk_level}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {sim.affected_components.length} components affected
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Impact;

// Made with Bob

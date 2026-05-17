/**
 * Query page for natural language Q&A
 */
import React, { useState } from 'react';
import { Send, MessageSquare, Clock } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';
import { queryCodebase } from '../api/endpoints';
import LoadingSpinner from '../components/LoadingSpinner';
import toast from 'react-hot-toast';

const Query: React.FC = () => {
  const { currentManifest, queryHistory, addQueryToHistory } = useAppStore();
  const [query, setQuery] = useState('');
  const [isQuerying, setIsQuerying] = useState(false);
  const [currentAnswer, setCurrentAnswer] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!currentManifest) {
      toast.error('Please upload a manifest file first');
      return;
    }

    if (!query.trim()) {
      toast.error('Please enter a question');
      return;
    }

    setIsQuerying(true);
    setCurrentAnswer(null);

    try {
      const result = await queryCodebase({
        manifest_path: currentManifest.path,
        manifest: currentManifest.content,
        query: query.trim(),
      });

      setCurrentAnswer(result);
      addQueryToHistory(result);
      setQuery('');
      toast.success('Query completed!');
    } catch (error: any) {
      toast.error(error?.error || 'Query failed');
      console.error('Query error:', error);
    } finally {
      setIsQuerying(false);
    }
  };

  const exampleQueries = [
    'What are the main components of this codebase?',
    'Which files have the most dependencies?',
    'Are there any security vulnerabilities?',
    'What is the overall code quality?',
    'Which modules are most complex?',
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Ask Questions
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Get AI-powered answers about your codebase
        </p>
      </div>

      {!currentManifest && (
        <div className="card text-center">
          <MessageSquare className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            No Manifest Loaded
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Please upload a repository manifest in the Analysis page first.
          </p>
        </div>
      )}

      {currentManifest && (
        <>
          {/* Query Form */}
          <div className="card">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Your Question
                </label>
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask anything about your codebase..."
                  rows={4}
                  className="input w-full resize-none"
                  disabled={isQuerying}
                />
              </div>
              <button
                type="submit"
                disabled={isQuerying || !query.trim()}
                className="btn-primary w-full inline-flex items-center justify-center gap-2"
              >
                {isQuerying ? (
                  <>
                    <LoadingSpinner size="sm" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    Ask Question
                  </>
                )}
              </button>
            </form>

            {/* Example Queries */}
            <div className="mt-6">
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Example questions:
              </p>
              <div className="flex flex-wrap gap-2">
                {exampleQueries.map((example, idx) => (
                  <button
                    key={idx}
                    onClick={() => setQuery(example)}
                    className="text-sm px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Current Answer */}
          {currentAnswer && (
            <div className="card">
              <div className="flex items-start gap-3 mb-4">
                <MessageSquare className="w-6 h-6 text-primary-600 dark:text-primary-400 flex-shrink-0 mt-1" />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Answer
                  </h3>
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                    {currentAnswer.answer}
                  </p>
                  <div className="mt-4 flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      <span>{currentAnswer.execution_time.toFixed(2)}s</span>
                    </div>
                    <div>
                      Confidence: {(currentAnswer.confidence * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Query History */}
          {queryHistory.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Recent Questions
              </h3>
              <div className="space-y-4">
                {queryHistory.slice(0, 5).map((item, idx) => (
                  <div
                    key={idx}
                    className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
                  >
                    <p className="font-medium text-gray-900 dark:text-white mb-2">
                      Q: {item.sources[0]?.query || 'Question'}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {item.answer.substring(0, 150)}
                      {item.answer.length > 150 && '...'}
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

export default Query;

// Made with Bob

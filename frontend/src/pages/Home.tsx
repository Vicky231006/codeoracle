/**
 * Home page component
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Code2, Zap, Shield, Brain, ArrowRight } from 'lucide-react';

const Home: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: Code2,
      title: 'Repository Mapping',
      description: 'Automatically analyze and map your entire codebase structure, dependencies, and relationships.',
      color: 'text-primary-600 dark:text-primary-400',
    },
    {
      icon: Brain,
      title: 'AI-Powered Insights',
      description: 'Ask natural language questions about your code and get intelligent, context-aware answers.',
      color: 'text-secondary-600 dark:text-secondary-400',
    },
    {
      icon: Shield,
      title: 'Risk Detection',
      description: 'Identify security vulnerabilities, code smells, and potential issues before they become problems.',
      color: 'text-danger-600 dark:text-danger-400',
    },
    {
      icon: Zap,
      title: 'Impact Simulation',
      description: 'Predict the impact of code changes across your entire system before making modifications.',
      color: 'text-warning-600 dark:text-warning-400',
    },
  ];

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-12">
        <div className="inline-flex items-center gap-3 mb-6">
          <Code2 className="w-16 h-16 text-primary-600 dark:text-primary-400" />
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white">
            CodeOracle
          </h1>
        </div>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
          AI-powered repository analysis that helps you understand, maintain, and improve your codebase with confidence.
        </p>
        <div className="flex gap-4 justify-center">
          <button
            onClick={() => navigate('/analysis')}
            className="btn-primary inline-flex items-center gap-2 text-lg px-8 py-3"
          >
            Get Started
            <ArrowRight className="w-5 h-5" />
          </button>
          <button
            onClick={() => navigate('/about')}
            className="btn-secondary text-lg px-8 py-3"
          >
            Learn More
          </button>
        </div>
      </section>

      {/* Features Grid */}
      <section>
        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-12">
          Powerful Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="card hover:shadow-xl transition-shadow"
            >
              <feature.icon className={`w-12 h-12 ${feature.color} mb-4`} />
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-8">
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">1</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Upload Manifest
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Provide your repository manifest JSON file or path
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">2</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              AI Analysis
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Our AI agents analyze your code structure and dependencies
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">3</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Get Insights
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Receive actionable insights and recommendations
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-center py-12 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg shadow-lg">
        <h2 className="text-3xl font-bold text-white mb-4">
          Ready to Transform Your Development Workflow?
        </h2>
        <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
          Start analyzing your codebase today and discover insights you never knew existed.
        </p>
        <button
          onClick={() => navigate('/analysis')}
          className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors inline-flex items-center gap-2"
        >
          Start Analysis
          <ArrowRight className="w-5 h-5" />
        </button>
      </section>
    </div>
  );
};

export default Home;

// Made with Bob

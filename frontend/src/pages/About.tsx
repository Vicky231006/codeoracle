/**
 * About page component
 */
import React from 'react';
import { Code2, Users, Zap, Shield, Brain, GitBranch } from 'lucide-react';

const About: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-12">
      <div className="text-center">
        <Code2 className="w-20 h-20 text-primary-600 dark:text-primary-400 mx-auto mb-4" />
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          About CodeOracle
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400">
          AI-powered repository analysis for modern development teams
        </p>
      </div>

      <div className="card">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          What is CodeOracle?
        </h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          CodeOracle is an advanced AI-powered tool designed to help development teams understand,
          maintain, and improve their codebases. Using state-of-the-art language models and
          sophisticated analysis techniques, CodeOracle provides deep insights into your code
          structure, dependencies, risks, and potential improvements.
        </p>
        <p className="text-gray-700 dark:text-gray-300">
          Built for the IBM BOB Hackathon, CodeOracle leverages IBM's Granite models to
          deliver accurate, context-aware analysis that helps teams make better decisions about
          their code.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <Brain className="w-10 h-10 text-primary-600 dark:text-primary-400 mb-3" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            AI-Powered Analysis
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Leverages IBM Granite models for intelligent code understanding and analysis
          </p>
        </div>

        <div className="card">
          <GitBranch className="w-10 h-10 text-secondary-600 dark:text-secondary-400 mb-3" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Dependency Mapping
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Visualize and understand complex dependency relationships in your codebase
          </p>
        </div>

        <div className="card">
          <Shield className="w-10 h-10 text-danger-600 dark:text-danger-400 mb-3" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Risk Detection
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Identify security vulnerabilities and code quality issues before they become problems
          </p>
        </div>

        <div className="card">
          <Zap className="w-10 h-10 text-warning-600 dark:text-warning-400 mb-3" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Impact Simulation
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Predict the impact of changes before implementation to reduce risks
          </p>
        </div>
      </div>

      <div className="card">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Key Features
        </h2>
        <ul className="space-y-3 text-gray-700 dark:text-gray-300">
          <li className="flex items-start gap-3">
            <span className="text-primary-600 dark:text-primary-400 font-bold">•</span>
            <span><strong>Repository Mapping:</strong> Automatically analyze and map your entire codebase structure</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="text-primary-600 dark:text-primary-400 font-bold">•</span>
            <span><strong>Natural Language Queries:</strong> Ask questions about your code in plain English</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="text-primary-600 dark:text-primary-400 font-bold">•</span>
            <span><strong>Dependency Analysis:</strong> Understand complex dependency relationships and identify issues</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="text-primary-600 dark:text-primary-400 font-bold">•</span>
            <span><strong>Risk Assessment:</strong> Get comprehensive risk scores and actionable recommendations</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="text-primary-600 dark:text-primary-400 font-bold">•</span>
            <span><strong>Impact Simulation:</strong> Predict the effects of code changes across your system</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="text-primary-600 dark:text-primary-400 font-bold">•</span>
            <span><strong>Multi-Agent Architecture:</strong> Specialized AI agents work together for comprehensive analysis</span>
          </li>
        </ul>
      </div>

      <div className="card">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Technology Stack
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="font-semibold text-gray-900 dark:text-white">IBM BOB Hackathon</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">AI Platform</p>
          </div>
          <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="font-semibold text-gray-900 dark:text-white">Granite Models</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">LLM</p>
          </div>
          <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="font-semibold text-gray-900 dark:text-white">FastAPI</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Backend</p>
          </div>
          <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="font-semibold text-gray-900 dark:text-white">React</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Frontend</p>
          </div>
          <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="font-semibold text-gray-900 dark:text-white">TypeScript</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Language</p>
          </div>
          <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="font-semibold text-gray-900 dark:text-white">TailwindCSS</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Styling</p>
          </div>
        </div>
      </div>

      <div className="card bg-gradient-to-r from-primary-600 to-secondary-600 text-white">
        <Users className="w-12 h-12 mb-4" />
        <h2 className="text-2xl font-bold mb-2">
          Built for Developers, by Developers
        </h2>
        <p className="text-white/90 mb-4">
          CodeOracle was created to solve real problems that development teams face every day.
          We understand the challenges of maintaining large codebases, and we're committed to
          making your development workflow more efficient and enjoyable.
        </p>
        <p className="text-white/90">
          Created for the IBM BOB Hackathon 2026
        </p>
      </div>
    </div>
  );
};

export default About;

// Made with Bob

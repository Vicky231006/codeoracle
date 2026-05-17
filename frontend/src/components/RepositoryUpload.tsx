/**
 * Repository manifest upload component
 */
import React, { useCallback, useState } from 'react';
import { Upload, FileJson, X, CheckCircle } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';
import toast from 'react-hot-toast';

interface RepositoryUploadProps {
  onUploadComplete?: (manifestPath: string) => void;
}

export const RepositoryUpload: React.FC<RepositoryUploadProps> = ({
  onUploadComplete,
}) => {
  const { setCurrentManifest } = useAppStore();
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [manifestPath, setManifestPath] = useState<string>('');

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    const jsonFile = files.find((f) => f.name.endsWith('.json'));

    if (jsonFile) {
      setSelectedFile(jsonFile);
    } else {
      toast.error('Please upload a JSON manifest file');
    }
  }, []);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.name.endsWith('.json')) {
        setSelectedFile(file);
      } else {
        toast.error('Please select a JSON manifest file');
      }
    }
  }, []);

  const handlePathSubmit = useCallback(() => {
    if (!manifestPath.trim()) {
      toast.error('Please enter a manifest path');
      return;
    }

    setCurrentManifest({
      path: manifestPath,
      name: manifestPath.split('/').pop() || manifestPath,
      size: 0,
      uploadedAt: new Date(),
    });

    toast.success('Manifest path set successfully');
    onUploadComplete?.(manifestPath);
  }, [manifestPath, setCurrentManifest, onUploadComplete]);

  const handleFileUpload = useCallback(async () => {
    if (!selectedFile) return;

    try {
      // For now, we'll use the file path directly
      // In production, you'd upload to the server
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const content = JSON.parse(reader.result as string);
          const path = selectedFile.name;
          setCurrentManifest({
            path,
            name: selectedFile.name,
            size: selectedFile.size,
            uploadedAt: new Date(),
            content,
          });

          toast.success('Manifest uploaded successfully');
          onUploadComplete?.(path);
        } catch (error) {
          toast.error('Invalid JSON file');
          console.error(error);
        }
      };
      reader.readAsText(selectedFile);
    } catch (error) {
      toast.error('Failed to upload manifest');
      console.error(error);
    }
  }, [selectedFile, setCurrentManifest, onUploadComplete]);

  const clearSelection = useCallback(() => {
    setSelectedFile(null);
  }, []);

  return (
    <div className="space-y-6">
      {/* File Upload */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
          Upload Manifest File
        </h3>
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            isDragging
              ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 dark:hover:border-primary-500'
          }`}
        >
          {selectedFile ? (
            <div className="space-y-4">
              <div className="flex items-center justify-center gap-3">
                <FileJson className="w-12 h-12 text-primary-600 dark:text-primary-400" />
                <div className="text-left">
                  <p className="font-medium text-gray-900 dark:text-white">
                    {selectedFile.name}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {(selectedFile.size / 1024).toFixed(2)} KB
                  </p>
                </div>
                <button
                  onClick={clearSelection}
                  className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                >
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>
              <button
                onClick={handleFileUpload}
                className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors inline-flex items-center gap-2"
              >
                <CheckCircle className="w-5 h-5" />
                Use This File
              </button>
            </div>
          ) : (
            <>
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 dark:text-gray-400 mb-2">
                Drag and drop your manifest JSON file here
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-500 mb-4">
                or
              </p>
              <label className="inline-block">
                <input
                  type="file"
                  accept=".json"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <span className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors cursor-pointer inline-block">
                  Browse Files
                </span>
              </label>
            </>
          )}
        </div>
      </div>

      {/* Divider */}
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-300 dark:border-gray-600"></div>
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-2 bg-white dark:bg-gray-800 text-gray-500">
            OR
          </span>
        </div>
      </div>

      {/* Path Input */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
          Enter Manifest Path
        </h3>
        <div className="flex gap-3">
          <input
            type="text"
            value={manifestPath}
            onChange={(e) => setManifestPath(e.target.value)}
            placeholder="/path/to/manifest.json"
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          <button
            onClick={handlePathSubmit}
            disabled={!manifestPath.trim()}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            Use Path
          </button>
        </div>
        <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
          Enter the absolute path to your repository manifest JSON file
        </p>
      </div>
    </div>
  );
};

export default RepositoryUpload;

// Made with Bob

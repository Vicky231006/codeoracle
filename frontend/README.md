# CodeOracle Frontend

Modern React-based web interface for CodeOracle repository analysis platform.

## 🚀 Features

- **Modern React 18** with TypeScript for type safety
- **Vite** for lightning-fast development and builds
- **TailwindCSS** for beautiful, responsive styling
- **Dark Mode** support with persistent preferences
- **State Management** using Zustand
- **API Integration** with Axios
- **Routing** with React Router v6
- **Toast Notifications** for user feedback
- **Error Boundaries** for graceful error handling
- **Responsive Design** for mobile, tablet, and desktop

## 📋 Prerequisites

- Node.js 18+ and npm/yarn
- CodeOracle API running on `http://localhost:8000`

## 🛠️ Installation

1. **Install dependencies:**
   ```bash
   cd codeoracle/frontend
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` if needed:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_API_TIMEOUT=30000
   VITE_ENABLE_DARK_MODE=true
   ```

## 🏃 Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Development Features

- **Hot Module Replacement (HMR)** - Instant updates without page refresh
- **TypeScript checking** - Real-time type validation
- **Fast Refresh** - Preserves component state during edits

## 🏗️ Build

Create a production build:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## 📁 Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── api/            # API client and endpoints
│   │   ├── client.ts   # Axios configuration
│   │   ├── endpoints.ts # API functions
│   │   └── types.ts    # TypeScript interfaces
│   ├── components/     # Reusable components
│   │   ├── AnalysisDashboard.tsx
│   │   ├── ErrorBoundary.tsx
│   │   ├── Header.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── RepositoryUpload.tsx
│   ├── pages/          # Page components
│   │   ├── About.tsx
│   │   ├── Analysis.tsx
│   │   ├── Home.tsx
│   │   ├── Impact.tsx
│   │   └── Query.tsx
│   ├── store/          # State management
│   │   └── useAppStore.ts
│   ├── App.tsx         # Main app component
│   ├── main.tsx        # Entry point
│   ├── index.css       # Global styles
│   └── vite-env.d.ts   # Vite type definitions
├── index.html          # HTML template
├── package.json        # Dependencies
├── tsconfig.json       # TypeScript config
├── vite.config.ts      # Vite config
└── tailwind.config.js  # Tailwind config
```

## 🎨 Components

### Core Components

#### Header
Navigation bar with dark mode toggle and responsive menu.

```tsx
import Header from './components/Header';
```

#### LoadingSpinner
Customizable loading indicator with optional text and full-screen mode.

```tsx
<LoadingSpinner size="lg" text="Loading..." fullScreen />
```

#### ErrorBoundary
Catches React errors and displays user-friendly error messages.

```tsx
<ErrorBoundary>
  <YourComponent />
</ErrorBoundary>
```

#### RepositoryUpload
File upload component with drag-and-drop support and path input.

```tsx
<RepositoryUpload onUploadComplete={(path) => console.log(path)} />
```

#### AnalysisDashboard
Displays comprehensive analysis results with cards and visualizations.

```tsx
<AnalysisDashboard />
```

## 📄 Pages

### Home (`/`)
Landing page with feature overview and call-to-action.

### Analysis (`/analysis`)
Main analysis page for uploading manifests and running analyses.

### Query (`/query`)
Natural language Q&A interface for codebase questions.

### Impact (`/impact`)
Impact simulation for predicting effects of code changes.

### About (`/about`)
Information about CodeOracle and its features.

## 🔌 API Integration

### API Client

The API client is configured in `src/api/client.ts`:

```typescript
import apiClient from './api/client';

// All requests automatically include:
// - Base URL from environment
// - Timeout configuration
// - Error handling
// - Request/response interceptors
```

### API Endpoints

All API functions are in `src/api/endpoints.ts`:

```typescript
import { analyzeRepository, queryCodebase, simulateImpact } from './api/endpoints';

// Analyze repository
const result = await analyzeRepository({
  manifest_path: '/path/to/manifest.json',
  analysis_depth: 'standard'
});

// Query codebase
const answer = await queryCodebase({
  manifest_path: '/path/to/manifest.json',
  query: 'What are the main components?'
});

// Simulate impact
const impact = await simulateImpact({
  manifest_path: '/path/to/manifest.json',
  change_description: 'Refactor authentication module',
  change_type: 'modification'
});
```

## 🗃️ State Management

Global state is managed with Zustand in `src/store/useAppStore.ts`:

```typescript
import { useAppStore } from './store/useAppStore';

function MyComponent() {
  const {
    currentManifest,
    setCurrentManifest,
    repositoryAnalysis,
    isDarkMode,
    toggleDarkMode
  } = useAppStore();

  // Use state...
}
```

### Available State

- `currentManifest` - Currently loaded manifest
- `repositoryAnalysis` - Repository analysis results
- `dependencyAnalysis` - Dependency analysis results
- `riskAssessment` - Risk assessment results
- `queryHistory` - Query history
- `impactSimulations` - Impact simulation history
- `isAnalyzing` - Loading state
- `error` - Error message
- `isDarkMode` - Dark mode preference

## 🎨 Styling

### TailwindCSS

Custom utility classes are defined in `src/index.css`:

```css
/* Button styles */
.btn-primary { /* Primary button */ }
.btn-secondary { /* Secondary button */ }

/* Card style */
.card { /* Card container */ }

/* Input style */
.input { /* Form input */ }
```

### Dark Mode

Dark mode is automatically applied based on user preference:

```tsx
// Toggle dark mode
const { toggleDarkMode } = useAppStore();

// Check dark mode state
const { isDarkMode } = useAppStore();
```

### Custom Colors

Defined in `tailwind.config.js`:

- `primary` - Blue shades
- `secondary` - Purple shades
- `success` - Green shades
- `warning` - Yellow/Orange shades
- `danger` - Red shades

## 🧪 Testing

Run tests:

```bash
npm test
```

Run tests with UI:

```bash
npm run test:ui
```

Generate coverage report:

```bash
npm run test:coverage
```

## 🔧 Configuration

### Vite Configuration

Edit `vite.config.ts` to customize:

- Build options
- Dev server settings
- Proxy configuration
- Plugin settings

### TypeScript Configuration

Edit `tsconfig.json` for:

- Compiler options
- Path aliases
- Type checking rules

### Tailwind Configuration

Edit `tailwind.config.js` for:

- Custom colors
- Font families
- Breakpoints
- Plugins

## 📦 Dependencies

### Core Dependencies

- `react` - UI library
- `react-dom` - React DOM renderer
- `react-router-dom` - Routing
- `axios` - HTTP client
- `zustand` - State management
- `lucide-react` - Icons
- `react-hot-toast` - Notifications
- `recharts` - Charts (optional)

### Dev Dependencies

- `vite` - Build tool
- `typescript` - Type checking
- `tailwindcss` - Styling
- `@vitejs/plugin-react` - React plugin
- `vitest` - Testing framework

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.

### Deploy to Static Hosting

The built files can be deployed to any static hosting service:

- **Vercel**: `vercel deploy`
- **Netlify**: Drag and drop `dist/` folder
- **GitHub Pages**: Use GitHub Actions
- **AWS S3**: Upload `dist/` to S3 bucket

### Environment Variables

Set these in your hosting platform:

```env
VITE_API_BASE_URL=https://your-api-domain.com
VITE_API_TIMEOUT=30000
```

## 🐛 Troubleshooting

### Port Already in Use

Change the port in `vite.config.ts`:

```typescript
server: {
  port: 3001, // Change to desired port
}
```

### API Connection Issues

1. Verify API is running on `http://localhost:8000`
2. Check CORS settings in API
3. Verify `VITE_API_BASE_URL` in `.env`

### Build Errors

1. Clear node_modules: `rm -rf node_modules && npm install`
2. Clear Vite cache: `rm -rf node_modules/.vite`
3. Update dependencies: `npm update`

## 📝 License

Part of the CodeOracle project for IBM BOB Hackathon 2026.

## 🤝 Contributing

This is a hackathon project. For improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Made with ❤️ for IBM BOB Hackathon 2026**
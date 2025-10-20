import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Home, History, Settings, BookOpen } from 'lucide-react';
import HomePage from './pages/HomePage';
import HistoryPage from './pages/HistoryPage';
import SettingsPage from './pages/SettingsPage';
import LearningPage from './pages/LearningPage';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-900 text-gray-100">
        {/* Sidebar */}
        <aside className="w-64 bg-gray-800 border-r border-gray-700">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-white mb-2">n8n 코드 생성기</h1>
            <p className="text-sm text-gray-400">완벽한 워크플로우 JSON</p>
          </div>
          
          <nav className="mt-6">
            <Link
              to="/"
              className="flex items-center px-6 py-3 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
            >
              <Home className="w-5 h-5 mr-3" />
              홈
            </Link>
            <Link
              to="/history"
              className="flex items-center px-6 py-3 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
            >
              <History className="w-5 h-5 mr-3" />
              히스토리
            </Link>
            <Link
              to="/learning"
              className="flex items-center px-6 py-3 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
            >
              <BookOpen className="w-5 h-5 mr-3" />
              학습 관리
            </Link>
            <Link
              to="/settings"
              className="flex items-center px-6 py-3 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
            >
              <Settings className="w-5 h-5 mr-3" />
              설정
            </Link>
          </nav>
        </aside>

        {/* Main content */}
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/learning" element={<LearningPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

import { useState, useEffect } from 'react';
import { Play, Database, TrendingUp, GitBranch } from 'lucide-react';
import { learningApi } from '../services/api';

export default function LearningPage() {
  const [stats, setStats] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [examples, setExamples] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsData, logsData, examplesData] = await Promise.all([
        learningApi.getStats(),
        learningApi.getLogs(0, 10),
        learningApi.listExamples(0, 20),
      ]);
      setStats(statsData);
      setLogs(logsData);
      setExamples(examplesData);
    } catch (error) {
      console.error('Failed to load learning data:', error);
    }
  };

  const handleRunLearning = async () => {
    if (!confirm('학습 사이클을 시작하시겠습니까? 몇 분이 소요될 수 있습니다.')) return;

    try {
      setLoading(true);
      await learningApi.runCycle();
      alert('학습이 백그라운드에서 시작되었습니다.');
      setTimeout(loadData, 5000); // Reload after 5 seconds
    } catch (error) {
      console.error('Failed to run learning:', error);
      alert('학습 시작에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full overflow-auto">
      <div className="bg-gray-800 border-b border-gray-700 px-8 py-4">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-semibold">학습 관리</h2>
            <p className="text-sm text-gray-400 mt-1">
              n8n 예제를 자동으로 학습하고 관리합니다
            </p>
          </div>
          <button
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors flex items-center space-x-2 disabled:opacity-50"
            onClick={handleRunLearning}
            disabled={loading}
          >
            <Play className="w-5 h-5" />
            <span>{loading ? '실행 중...' : '수동 학습 시작'}</span>
          </button>
        </div>
      </div>

      <div className="p-8">
        <div className="max-w-6xl mx-auto space-y-6">
          {/* Statistics */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gray-800 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">총 학습 예제</h3>
                  <Database className="w-8 h-8 text-blue-400" />
                </div>
                <p className="text-3xl font-bold text-blue-400">{stats.total_examples}</p>
              </div>

              <div className="bg-gray-800 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">소스별 분포</h3>
                  <TrendingUp className="w-8 h-8 text-green-400" />
                </div>
                <div className="space-y-2 text-sm">
                  {Object.entries(stats.by_source).map(([source, count]) => (
                    <div key={source} className="flex justify-between">
                      <span className="text-gray-400">{source}:</span>
                      <span className="text-white font-medium">{count as number}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-gray-800 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">복잡도별</h3>
                  <GitBranch className="w-8 h-8 text-purple-400" />
                </div>
                <div className="space-y-2 text-sm">
                  {Object.entries(stats.by_complexity).map(([level, count]) => (
                    <div key={level} className="flex justify-between">
                      <span className="text-gray-400">{level}:</span>
                      <span className="text-white font-medium">{count as number}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Top Nodes */}
          {stats && stats.top_nodes && Object.keys(stats.top_nodes).length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">가장 많이 사용되는 노드</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(stats.top_nodes)
                  .slice(0, 12)
                  .map(([node, count]) => (
                    <div key={node} className="bg-gray-900 rounded p-3">
                      <div className="text-sm font-medium text-gray-300 truncate">{node}</div>
                      <div className="text-xs text-gray-500 mt-1">사용 횟수: {count as number}</div>
                    </div>
                  ))}
              </div>
            </div>
          )}

          {/* Learning Logs */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4">학습 로그</h3>
            {logs.length === 0 ? (
              <p className="text-gray-400 text-center py-4">학습 로그가 없습니다</p>
            ) : (
              <div className="space-y-3">
                {logs.map((log) => (
                  <div key={log.id} className="bg-gray-900 rounded p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <span className="text-sm font-medium text-gray-300">
                          {log.learning_type === 'docs'
                            ? '공식 문서'
                            : log.learning_type === 'github'
                            ? 'GitHub'
                            : '템플릿'}
                        </span>
                        <span
                          className={`ml-3 text-xs px-2 py-1 rounded ${
                            log.status === 'completed'
                              ? 'bg-green-900 text-green-300'
                              : log.status === 'failed'
                              ? 'bg-red-900 text-red-300'
                              : 'bg-blue-900 text-blue-300'
                          }`}
                        >
                          {log.status === 'completed'
                            ? '완료'
                            : log.status === 'failed'
                            ? '실패'
                            : '진행 중'}
                        </span>
                      </div>
                      <span className="text-xs text-gray-500">
                        {new Date(log.started_at).toLocaleString('ko-KR')}
                      </span>
                    </div>
                    <div className="text-sm text-gray-400">
                      발견: {log.examples_found}개 | 추가: {log.examples_added}개
                    </div>
                    {log.error_message && (
                      <div className="mt-2 text-xs text-red-400">{log.error_message}</div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Recent Examples */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4">최근 학습한 예제</h3>
            {examples.length === 0 ? (
              <p className="text-gray-400 text-center py-4">학습된 예제가 없습니다</p>
            ) : (
              <div className="grid gap-4">
                {examples.map((example) => (
                  <div key={example.id} className="bg-gray-900 rounded p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-gray-300">{example.title}</h4>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs px-2 py-1 bg-blue-900 text-blue-300 rounded">
                          {example.source}
                        </span>
                        {example.complexity_level && (
                          <span
                            className={`text-xs px-2 py-1 rounded ${
                              example.complexity_level === 'simple'
                                ? 'bg-green-900 text-green-300'
                                : example.complexity_level === 'medium'
                                ? 'bg-yellow-900 text-yellow-300'
                                : 'bg-red-900 text-red-300'
                            }`}
                          >
                            {example.complexity_level}
                          </span>
                        )}
                      </div>
                    </div>
                    {example.description && (
                      <p className="text-sm text-gray-400 mb-2">{example.description}</p>
                    )}
                    {example.nodes_used && example.nodes_used.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {example.nodes_used.slice(0, 8).map((node: string, idx: number) => (
                          <span
                            key={idx}
                            className="text-xs px-2 py-1 bg-gray-800 text-gray-300 rounded"
                          >
                            {node}
                          </span>
                        ))}
                        {example.nodes_used.length > 8 && (
                          <span className="text-xs px-2 py-1 text-gray-500">
                            +{example.nodes_used.length - 8}
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

import { useState, useEffect } from 'react';
import { Clock, Eye, Download } from 'lucide-react';
import Editor from '@monaco-editor/react';
import { workflowApi, WorkflowRequest } from '../services/api';

export default function HistoryPage() {
  const [workflows, setWorkflows] = useState<WorkflowRequest[]>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState<WorkflowRequest | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadWorkflows();
  }, []);

  const loadWorkflows = async () => {
    try {
      setLoading(true);
      const result = await workflowApi.list(0, 50);
      setWorkflows(result.items);
    } catch (error) {
      console.error('Failed to load workflows:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      completed: 'text-green-400',
      failed: 'text-red-400',
      pending: 'text-gray-400',
      analyzing: 'text-blue-400',
      generating_json: 'text-purple-400',
      testing: 'text-yellow-400',
    };
    return colors[status] || 'text-gray-400';
  };

  const getStatusText = (status: string) => {
    const texts: Record<string, string> = {
      completed: '완료',
      failed: '실패',
      pending: '대기 중',
      analyzing: '분석 중',
      awaiting_answers: '답변 대기',
      generating_spec: '요구서 생성 중',
      spec_review: '요구서 검토',
      spec_approved: '요구서 승인됨',
      generating_json: 'JSON 생성 중',
      testing: '테스트 중',
    };
    return texts[status] || status;
  };

  const downloadJson = (workflow: WorkflowRequest) => {
    const json = workflow.final_json || workflow.generated_json;
    if (!json) return;

    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `n8n-workflow-${workflow.id}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="h-full flex">
      {/* Workflows List */}
      <div className="w-1/3 border-r border-gray-700 overflow-auto">
        <div className="bg-gray-800 border-b border-gray-700 px-6 py-4">
          <h2 className="text-xl font-semibold">워크플로우 히스토리</h2>
          <p className="text-sm text-gray-400 mt-1">
            생성한 워크플로우 목록: {workflows.length}개
          </p>
        </div>

        {loading ? (
          <div className="p-6 text-center text-gray-400">로딩 중...</div>
        ) : workflows.length === 0 ? (
          <div className="p-6 text-center text-gray-400">
            생성된 워크플로우가 없습니다.
          </div>
        ) : (
          <div className="divide-y divide-gray-700">
            {workflows.map((workflow) => (
              <div
                key={workflow.id}
                className={`p-4 cursor-pointer hover:bg-gray-800 transition-colors ${
                  selectedWorkflow?.id === workflow.id ? 'bg-gray-800' : ''
                }`}
                onClick={() => setSelectedWorkflow(workflow)}
              >
                <div className="flex items-start justify-between mb-2">
                  <span className="text-sm font-medium text-gray-300">
                    Workflow #{workflow.id}
                  </span>
                  <span className={`text-xs ${getStatusColor(workflow.status)}`}>
                    {getStatusText(workflow.status)}
                  </span>
                </div>
                <p className="text-sm text-gray-400 line-clamp-2 mb-2">
                  {workflow.user_requirement}
                </p>
                <div className="flex items-center text-xs text-gray-500">
                  <Clock className="w-3 h-3 mr-1" />
                  {new Date(workflow.created_at).toLocaleString('ko-KR')}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Workflow Detail */}
      <div className="flex-1 overflow-auto">
        {selectedWorkflow ? (
          <div className="p-6">
            <div className="bg-gray-800 rounded-lg p-6 mb-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold mb-2">
                    Workflow #{selectedWorkflow.id}
                  </h3>
                  <span className={`text-sm ${getStatusColor(selectedWorkflow.status)}`}>
                    {getStatusText(selectedWorkflow.status)}
                  </span>
                </div>
                {(selectedWorkflow.final_json || selectedWorkflow.generated_json) && (
                  <button
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded transition-colors flex items-center space-x-2"
                    onClick={() => downloadJson(selectedWorkflow)}
                  >
                    <Download className="w-4 h-4" />
                    <span>다운로드</span>
                  </button>
                )}
              </div>

              <div className="space-y-4 text-sm">
                <div>
                  <span className="text-gray-400 font-medium">생성일:</span>
                  <span className="ml-2 text-gray-300">
                    {new Date(selectedWorkflow.created_at).toLocaleString('ko-KR')}
                  </span>
                </div>
                <div>
                  <span className="text-gray-400 font-medium">요구사항:</span>
                  <p className="mt-2 text-gray-300 whitespace-pre-wrap">
                    {selectedWorkflow.user_requirement}
                  </p>
                </div>
              </div>
            </div>

            {selectedWorkflow.development_spec && (
              <div className="bg-gray-800 rounded-lg p-6 mb-6">
                <h4 className="text-lg font-semibold mb-3">개발요구서</h4>
                <div className="bg-gray-900 rounded p-4 text-sm text-gray-300 whitespace-pre-wrap max-h-96 overflow-auto">
                  {selectedWorkflow.development_spec}
                </div>
              </div>
            )}

            {(selectedWorkflow.final_json || selectedWorkflow.generated_json) && (
              <div className="bg-gray-800 rounded-lg p-6">
                <h4 className="text-lg font-semibold mb-3">n8n 워크플로우 JSON</h4>
                <div className="border border-gray-700 rounded-lg overflow-hidden">
                  <Editor
                    height="500px"
                    defaultLanguage="json"
                    value={selectedWorkflow.final_json || selectedWorkflow.generated_json}
                    theme="vs-dark"
                    options={{
                      readOnly: true,
                      minimap: { enabled: false },
                      fontSize: 14,
                      lineNumbers: 'on',
                      scrollBeyondLastLine: false,
                      automaticLayout: true,
                    }}
                  />
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-400">
            <div className="text-center">
              <Eye className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p>워크플로우를 선택하여 상세 내용을 확인하세요</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

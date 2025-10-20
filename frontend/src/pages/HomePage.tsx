import { useState, useEffect } from 'react';
import { Send, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import Editor from '@monaco-editor/react';
import { workflowApi, Answer } from '../services/api';
import { useWorkflowStore } from '../store/workflowStore';

type Step =
  | 'input'
  | 'analyzing'
  | 'questions'
  | 'generating_spec'
  | 'spec_review'
  | 'generating_json'
  | 'testing'
  | 'completed';

export default function HomePage() {
  const [requirement, setRequirement] = useState('');
  const [currentStep, setCurrentStep] = useState<Step>('input');
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [developmentSpec, setDevelopmentSpec] = useState('');
  const [generatedJson, setGeneratedJson] = useState('');
  const [finalJson, setFinalJson] = useState('');
  const [testResults, setTestResults] = useState<any>(null);
  const [error, setError] = useState('');
  
  const { currentWorkflow, setCurrentWorkflow } = useWorkflowStore();

  const handleSubmitRequirement = async () => {
    if (!requirement.trim()) return;

    try {
      setCurrentStep('analyzing');
      setError('');

      // Create workflow request
      const workflow = await workflowApi.create({ requirement });
      setCurrentWorkflow(workflow);

      // Analyze requirement
      const analysis = await workflowApi.analyze(workflow.id);
      
      if (analysis.questions && analysis.questions.length > 0) {
        setQuestions(analysis.questions);
        setCurrentStep('questions');
      } else {
        // No questions, proceed to spec generation
        await handleGenerateSpec(workflow.id);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '오류가 발생했습니다.');
      setCurrentStep('input');
    }
  };

  const handleSubmitAnswers = async () => {
    if (!currentWorkflow) return;

    try {
      setCurrentStep('generating_spec');
      
      const answersArray: Answer[] = Object.entries(answers).map(([qId, ans]) => ({
        question_id: qId,
        answer: ans,
      }));

      await workflowApi.submitAnswers(currentWorkflow.id, answersArray);
      await handleGenerateSpec(currentWorkflow.id);
    } catch (err: any) {
      setError(err.response?.data?.detail || '오류가 발생했습니다.');
    }
  };

  const handleGenerateSpec = async (workflowId: number) => {
    try {
      const result = await workflowApi.generateSpec(workflowId);
      setDevelopmentSpec(result.development_spec);
      setCurrentStep('spec_review');
    } catch (err: any) {
      setError(err.response?.data?.detail || '개발요구서 생성 중 오류가 발생했습니다.');
    }
  };

  const handleApproveSpec = async () => {
    if (!currentWorkflow) return;

    try {
      setCurrentStep('generating_json');
      
      // Update spec if modified
      await workflowApi.updateSpec(currentWorkflow.id, developmentSpec);
      
      // Generate JSON
      const result = await workflowApi.generateJson(currentWorkflow.id);
      setGeneratedJson(result.workflow_json);
      
      // Test and optimize
      setCurrentStep('testing');
      const testResult = await workflowApi.testAndOptimize(currentWorkflow.id);
      setTestResults(testResult);
      
      // Get final JSON
      if (testResult.optimized_json) {
        setFinalJson(testResult.optimized_json);
      } else {
        setFinalJson(result.workflow_json);
      }
      
      setCurrentStep('completed');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'JSON 생성 중 오류가 발생했습니다.');
    }
  };

  const handleReset = () => {
    setRequirement('');
    setCurrentStep('input');
    setQuestions([]);
    setAnswers({});
    setDevelopmentSpec('');
    setGeneratedJson('');
    setFinalJson('');
    setTestResults(null);
    setError('');
    setCurrentWorkflow(null);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert('클립보드에 복사되었습니다!');
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700 px-8 py-4">
        <h2 className="text-2xl font-semibold">n8n 워크플로우 생성</h2>
        <p className="text-sm text-gray-400 mt-1">
          요구사항을 입력하면 완벽한 n8n JSON 코드를 생성합니다
        </p>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-8">
        <div className="max-w-6xl mx-auto space-y-6">
          {/* Step 1: Input Requirement */}
          {currentStep === 'input' && (
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
              <h3 className="text-xl font-semibold mb-4">1. 요구사항 입력</h3>
              <textarea
                className="w-full h-48 px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                placeholder="만들고 싶은 n8n 워크플로우를 자유롭게 설명해주세요...&#10;&#10;예시:&#10;- 매일 아침 9시에 Gmail에서 미읽은 메일을 확인하고, 중요한 메일이 있으면 Slack으로 알림을 보내주세요&#10;- 구글 시트에 새로운 행이 추가되면 자동으로 Notion 데이터베이스에 추가해주세요&#10;- 특정 키워드가 포함된 트윗을 실시간으로 모니터링하고 Discord에 알림을 보내주세요"
                value={requirement}
                onChange={(e) => setRequirement(e.target.value)}
              />
              <button
                className="mt-4 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors flex items-center space-x-2"
                onClick={handleSubmitRequirement}
                disabled={!requirement.trim()}
              >
                <Send className="w-5 h-5" />
                <span>분석 시작</span>
              </button>
              {error && (
                <div className="mt-4 p-4 bg-red-900/50 border border-red-700 rounded-lg flex items-start space-x-2">
                  <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                  <p className="text-red-200">{error}</p>
                </div>
              )}
            </div>
          )}

          {/* Step 2: Analyzing */}
          {currentStep === 'analyzing' && (
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg text-center">
              <Loader2 className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">요구사항 분석 중...</h3>
              <p className="text-gray-400">AI가 여러분의 요구사항을 분석하고 있습니다.</p>
            </div>
          )}

          {/* Step 3: Questions */}
          {currentStep === 'questions' && questions.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
              <h3 className="text-xl font-semibold mb-4">2. 추가 정보 제공</h3>
              <p className="text-gray-400 mb-6">
                더 정확한 워크플로우 생성을 위해 몇 가지 질문에 답해주세요.
              </p>
              <div className="space-y-4">
                {questions.map((q, idx) => (
                  <div key={q.id} className="space-y-2">
                    <label className="block text-sm font-medium text-gray-300">
                      {idx + 1}. {q.question}
                      {q.required && <span className="text-red-400 ml-1">*</span>}
                    </label>
                    {q.question_type === 'text' && (
                      <textarea
                        className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                        rows={3}
                        value={answers[q.id] || ''}
                        onChange={(e) =>
                          setAnswers({ ...answers, [q.id]: e.target.value })
                        }
                      />
                    )}
                    {q.question_type === 'choice' && q.options && (
                      <select
                        className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value={answers[q.id] || ''}
                        onChange={(e) =>
                          setAnswers({ ...answers, [q.id]: e.target.value })
                        }
                      >
                        <option value="">선택하세요</option>
                        {q.options.map((opt: string) => (
                          <option key={opt} value={opt}>
                            {opt}
                          </option>
                        ))}
                      </select>
                    )}
                  </div>
                ))}
              </div>
              <button
                className="mt-6 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
                onClick={handleSubmitAnswers}
              >
                다음 단계
              </button>
            </div>
          )}

          {/* Step 4: Generating Spec */}
          {currentStep === 'generating_spec' && (
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg text-center">
              <Loader2 className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">개발요구서 생성 중...</h3>
              <p className="text-gray-400">
                수집된 정보를 바탕으로 상세한 개발요구서를 작성하고 있습니다.
              </p>
            </div>
          )}

          {/* Step 5: Spec Review */}
          {currentStep === 'spec_review' && (
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
              <h3 className="text-xl font-semibold mb-4">3. 개발요구서 검토</h3>
              <p className="text-gray-400 mb-4">
                생성된 개발요구서를 검토하고 필요시 수정하세요.
              </p>
              <textarea
                className="w-full h-96 px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                value={developmentSpec}
                onChange={(e) => setDevelopmentSpec(e.target.value)}
              />
              <button
                className="mt-4 px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors"
                onClick={handleApproveSpec}
              >
                승인 및 JSON 생성
              </button>
            </div>
          )}

          {/* Step 6-7: Generating and Testing */}
          {(currentStep === 'generating_json' || currentStep === 'testing') && (
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg text-center">
              <Loader2 className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">
                {currentStep === 'generating_json'
                  ? 'n8n JSON 코드 생성 중...'
                  : '생성된 코드 테스트 및 최적화 중...'}
              </h3>
              <p className="text-gray-400">잠시만 기다려주세요.</p>
            </div>
          )}

          {/* Step 8: Completed */}
          {currentStep === 'completed' && (
            <div className="space-y-6">
              <div className="bg-green-900/30 border border-green-700 rounded-lg p-6 flex items-center space-x-3">
                <CheckCircle className="w-8 h-8 text-green-400" />
                <div>
                  <h3 className="text-xl font-semibold text-green-300">완료!</h3>
                  <p className="text-green-200">
                    n8n 워크플로우 JSON 코드가 성공적으로 생성되었습니다.
                  </p>
                </div>
              </div>

              {/* Test Results */}
              {testResults && (
                <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
                  <h3 className="text-lg font-semibold mb-3">테스트 결과</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center space-x-2">
                      <span className="text-gray-400">상태:</span>
                      <span
                        className={
                          testResults.passed ? 'text-green-400' : 'text-yellow-400'
                        }
                      >
                        {testResults.passed ? '통과' : '주의사항 있음'}
                      </span>
                    </div>
                    {testResults.issues && testResults.issues.length > 0 && (
                      <div>
                        <span className="text-gray-400">발견된 문제:</span>
                        <ul className="list-disc list-inside ml-4 mt-1 text-yellow-400">
                          {testResults.issues.map((issue: string, idx: number) => (
                            <li key={idx}>{issue}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {testResults.suggestions && testResults.suggestions.length > 0 && (
                      <div>
                        <span className="text-gray-400">개선 제안:</span>
                        <ul className="list-disc list-inside ml-4 mt-1 text-blue-400">
                          {testResults.suggestions.map((sug: string, idx: number) => (
                            <li key={idx}>{sug}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Final JSON */}
              <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">최종 n8n 워크플로우 JSON</h3>
                  <button
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded transition-colors"
                    onClick={() => copyToClipboard(finalJson)}
                  >
                    복사
                  </button>
                </div>
                <div className="border border-gray-700 rounded-lg overflow-hidden">
                  <Editor
                    height="500px"
                    defaultLanguage="json"
                    value={finalJson}
                    theme="vs-dark"
                    options={{
                      readOnly: false,
                      minimap: { enabled: false },
                      fontSize: 14,
                      lineNumbers: 'on',
                      scrollBeyondLastLine: false,
                      automaticLayout: true,
                    }}
                    onChange={(value) => setFinalJson(value || '')}
                  />
                </div>
              </div>

              <button
                className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-medium rounded-lg transition-colors"
                onClick={handleReset}
              >
                새로운 워크플로우 생성
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

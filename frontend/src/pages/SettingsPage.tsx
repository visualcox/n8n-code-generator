import { useState, useEffect } from 'react';
import { Plus, Trash2, Check, Settings } from 'lucide-react';
import { llmConfigApi, LLMConfig } from '../services/api';

export default function SettingsPage() {
  const [configs, setConfigs] = useState<LLMConfig[]>([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newConfig, setNewConfig] = useState<Partial<LLMConfig>>({
    name: '',
    provider: 'openai',
    model_name: 'gpt-4-turbo-preview',
    temperature: 70,
    max_tokens: 4000,
    is_default: false,
  });

  useEffect(() => {
    loadConfigs();
  }, []);

  const loadConfigs = async () => {
    try {
      const data = await llmConfigApi.list();
      setConfigs(data);
    } catch (error) {
      console.error('Failed to load configs:', error);
    }
  };

  const handleAddConfig = async () => {
    try {
      await llmConfigApi.create(newConfig as LLMConfig);
      setShowAddForm(false);
      setNewConfig({
        name: '',
        provider: 'openai',
        model_name: 'gpt-4-turbo-preview',
        temperature: 70,
        max_tokens: 4000,
        is_default: false,
      });
      loadConfigs();
    } catch (error) {
      console.error('Failed to add config:', error);
    }
  };

  const handleActivate = async (configId: number) => {
    try {
      await llmConfigApi.activate(configId);
      loadConfigs();
    } catch (error) {
      console.error('Failed to activate config:', error);
    }
  };

  const handleDelete = async (configId: number) => {
    if (!confirm('정말로 이 설정을 삭제하시겠습니까?')) return;
    
    try {
      await llmConfigApi.delete(configId);
      loadConfigs();
    } catch (error) {
      console.error('Failed to delete config:', error);
    }
  };

  return (
    <div className="h-full overflow-auto">
      <div className="bg-gray-800 border-b border-gray-700 px-8 py-4">
        <h2 className="text-2xl font-semibold">LLM 설정</h2>
        <p className="text-sm text-gray-400 mt-1">
          워크플로우 생성에 사용할 LLM을 설정합니다
        </p>
      </div>

      <div className="p-8">
        <div className="max-w-4xl mx-auto space-y-6">
          {/* Add Config Button */}
          <button
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors flex items-center space-x-2"
            onClick={() => setShowAddForm(!showAddForm)}
          >
            <Plus className="w-5 h-5" />
            <span>새 LLM 설정 추가</span>
          </button>

          {/* Add Config Form */}
          {showAddForm && (
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">새 LLM 설정</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    설정 이름
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={newConfig.name}
                    onChange={(e) => setNewConfig({ ...newConfig, name: e.target.value })}
                    placeholder="예: My OpenAI GPT-4"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    제공자
                  </label>
                  <select
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={newConfig.provider}
                    onChange={(e) => setNewConfig({ ...newConfig, provider: e.target.value })}
                  >
                    <option value="openai">OpenAI</option>
                    <option value="anthropic">Anthropic</option>
                    <option value="ollama">Ollama (로컬)</option>
                    <option value="custom">커스텀</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    모델 이름
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={newConfig.model_name}
                    onChange={(e) => setNewConfig({ ...newConfig, model_name: e.target.value })}
                    placeholder="예: gpt-4-turbo-preview"
                  />
                </div>

                {newConfig.provider !== 'ollama' && (
                  <div className="col-span-2">
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      API Key
                    </label>
                    <input
                      type="password"
                      className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      value={newConfig.api_key || ''}
                      onChange={(e) => setNewConfig({ ...newConfig, api_key: e.target.value })}
                      placeholder="API 키를 입력하세요"
                    />
                  </div>
                )}

                {(newConfig.provider === 'ollama' || newConfig.provider === 'custom') && (
                  <div className="col-span-2">
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      API URL
                    </label>
                    <input
                      type="text"
                      className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      value={newConfig.api_url || ''}
                      onChange={(e) => setNewConfig({ ...newConfig, api_url: e.target.value })}
                      placeholder="예: http://localhost:11434"
                    />
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Temperature ({newConfig.temperature}%)
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    className="w-full"
                    value={newConfig.temperature}
                    onChange={(e) =>
                      setNewConfig({ ...newConfig, temperature: parseInt(e.target.value) })
                    }
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Max Tokens
                  </label>
                  <input
                    type="number"
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={newConfig.max_tokens}
                    onChange={(e) =>
                      setNewConfig({ ...newConfig, max_tokens: parseInt(e.target.value) })
                    }
                  />
                </div>

                <div className="col-span-2">
                  <label className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      className="w-4 h-4 text-blue-600 bg-gray-900 border-gray-700 rounded focus:ring-blue-500"
                      checked={newConfig.is_default}
                      onChange={(e) =>
                        setNewConfig({ ...newConfig, is_default: e.target.checked })
                      }
                    />
                    <span className="text-sm text-gray-300">기본 설정으로 사용</span>
                  </label>
                </div>
              </div>

              <div className="mt-6 flex space-x-3">
                <button
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
                  onClick={handleAddConfig}
                >
                  추가
                </button>
                <button
                  className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white font-medium rounded-lg transition-colors"
                  onClick={() => setShowAddForm(false)}
                >
                  취소
                </button>
              </div>
            </div>
          )}

          {/* Configs List */}
          <div className="space-y-4">
            {configs.length === 0 ? (
              <div className="bg-gray-800 rounded-lg p-8 text-center text-gray-400">
                <Settings className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>설정된 LLM이 없습니다</p>
                <p className="text-sm mt-1">새 LLM 설정을 추가해주세요</p>
              </div>
            ) : (
              configs.map((config) => (
                <div
                  key={config.id}
                  className={`bg-gray-800 rounded-lg p-6 border-2 ${
                    config.is_active ? 'border-blue-500' : 'border-transparent'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-semibold">{config.name}</h3>
                        {config.is_active && (
                          <span className="px-2 py-1 bg-blue-600 text-xs text-white rounded">
                            활성
                          </span>
                        )}
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-sm text-gray-400">
                        <div>
                          <span className="font-medium">제공자:</span> {config.provider}
                        </div>
                        <div>
                          <span className="font-medium">모델:</span> {config.model_name}
                        </div>
                        <div>
                          <span className="font-medium">Temperature:</span> {config.temperature}%
                        </div>
                        <div>
                          <span className="font-medium">Max Tokens:</span> {config.max_tokens}
                        </div>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      {!config.is_active && (
                        <button
                          className="p-2 text-green-400 hover:bg-gray-700 rounded transition-colors"
                          onClick={() => handleActivate(config.id!)}
                          title="활성화"
                        >
                          <Check className="w-5 h-5" />
                        </button>
                      )}
                      <button
                        className="p-2 text-red-400 hover:bg-gray-700 rounded transition-colors"
                        onClick={() => handleDelete(config.id!)}
                        title="삭제"
                      >
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

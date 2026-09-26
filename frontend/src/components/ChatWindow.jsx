import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, AlertCircle, Loader2 } from 'lucide-react';
import { askQuestion } from '../api/client';
import { SourceCard } from './SourceCard';

export const ChatWindow = ({ apiKey }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I am your Research Paper Answer Bot powered by RAG and Google Gemini. Ask me any question about the loaded AI/Data Science papers, and I will provide grounded answers with page references!',
      sources: []
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const sampleQuestions = [
    "What is the main architecture proposed in Attention Is All You Need?",
    "Why are residual connections effective in deep neural networks?",
    "Compare positional encoding vs recurrent layers in sequence modeling."
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (queryText) => {
    const query = queryText || input;
    if (!query.trim() || loading) return;

    const userMessage = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await askQuestion(query, apiKey);
      const botMessage = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources || []
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const errorMessage = {
        role: 'assistant',
        content: err.response?.data?.detail || 'An error occurred while communicating with the RAG backend server.',
        isError: true,
        sources: []
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="messages-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message-row ${msg.role}`}>
            <div className="avatar">
              {msg.role === 'assistant' ? <Bot size={20} /> : <User size={20} />}
            </div>
            <div className={`message-bubble ${msg.isError ? 'error-bubble' : ''}`}>
              <div className="message-text">{msg.content}</div>
              
              {msg.sources && msg.sources.length > 0 && (
                <div className="sources-section">
                  <span className="sources-label">Reference Citations:</span>
                  <div className="sources-grid">
                    {msg.sources.map((src, sIdx) => (
                      <SourceCard key={sIdx} source={src} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-row assistant">
            <div className="avatar">
              <Bot size={20} />
            </div>
            <div className="message-bubble loading-bubble">
              <Loader2 size={18} className="spin" />
              <span>Searching research papers & generating answer with Gemini...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {messages.length <= 2 && (
        <div className="sample-prompts">
          <span className="prompts-label"><Sparkles size={14} /> Try asking:</span>
          <div className="prompts-list">
            {sampleQuestions.map((q, idx) => (
              <button key={idx} className="prompt-chip" onClick={() => handleSend(q)}>
                "{q}"
              </button>
            ))}
          </div>
        </div>
      )}

      <form className="chat-input-form" onSubmit={(e) => { e.preventDefault(); handleSend(); }}>
        <input
          type="text"
          className="chat-input"
          placeholder="Ask a question about the research papers..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" className="send-btn" disabled={!input.trim() || loading}>
          <Send size={18} />
        </button>
      </form>
    </div>
  );
};

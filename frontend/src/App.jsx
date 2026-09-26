import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatWindow } from './components/ChatWindow';
import { fetchPapers } from './api/client';
import { Sparkles } from 'lucide-react';
import './App.css';

export function App() {
  const [papers, setPapers] = useState([]);
  const [apiKey, setApiKey] = useState('');

  const loadPapersList = async () => {
    try {
      const list = await fetchPapers();
      setPapers(list);
    } catch (err) {
      console.error("Failed to load papers:", err);
    }
  };

  useEffect(() => {
    loadPapersList();
  }, []);

  return (
    <div className="app-container">
      <header className="main-header">
        <div className="header-brand">
          <Sparkles className="brand-icon" />
          <h1>Research Paper Answer Bot</h1>
          <span className="badge">RAG + Gemini</span>
        </div>
        <p className="header-subtitle">
          Grounded Q&A on AI & Data Science Research Papers with Page Citations
        </p>
      </header>

      <div className="main-layout">
        <Sidebar 
          papers={papers} 
          refreshPapers={loadPapersList}
          apiKey={apiKey}
          setApiKey={setApiKey}
        />
        <main className="content-area">
          <ChatWindow apiKey={apiKey} />
        </main>
      </div>
    </div>
  );
}

export default App;

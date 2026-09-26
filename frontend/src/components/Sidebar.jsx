import React, { useRef, useState } from 'react';
import { BookOpen, Upload, Key, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';
import { uploadPaper } from '../api/client';

export const Sidebar = ({ papers, refreshPapers, apiKey, setApiKey }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.pdf')) {
      setUploadMessage({ type: 'error', text: 'Please select a valid PDF file.' });
      return;
    }

    setUploading(true);
    setUploadMessage(null);

    try {
      const res = await uploadPaper(file, apiKey);
      setUploadMessage({ type: 'success', text: `Uploaded & indexed: ${file.name}` });
      refreshPapers();
    } catch (err) {
      setUploadMessage({ type: 'error', text: err.response?.data?.detail || 'Upload failed.' });
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2><BookOpen className="icon" /> Paper Library</h2>
      </div>

      <div className="sidebar-section">
        <label className="section-label">
          <Key size={14} /> Gemini API Key (Optional Override)
        </label>
        <input
          type="password"
          className="api-input"
          placeholder="Paste API Key if not in .env..."
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
        <span className="api-hint">Key stays local in browser</span>
      </div>

      <div className="sidebar-section">
        <div className="section-title-row">
          <label className="section-label">Curated Research Papers ({papers.length})</label>
          <button className="refresh-btn" onClick={refreshPapers} title="Refresh list">
            <RefreshCw size={14} />
          </button>
        </div>

        {papers.length === 0 ? (
          <p className="empty-text">No papers indexed yet.</p>
        ) : (
          <ul className="paper-list">
            {papers.map((paper, idx) => (
              <li key={idx} className="paper-item">
                <BookOpen size={14} />
                <span className="paper-name" title={paper}>{paper}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="sidebar-section upload-section">
        <label className="section-label">Upload New PDF Paper</label>
        <input
          type="file"
          accept=".pdf"
          ref={fileInputRef}
          onChange={handleFileUpload}
          style={{ display: 'none' }}
        />
        <button 
          className="upload-btn" 
          disabled={uploading}
          onClick={() => fileInputRef.current?.click()}
        >
          {uploading ? <RefreshCw size={16} className="spin" /> : <Upload size={16} />}
          {uploading ? 'Processing PDF...' : 'Upload PDF Paper'}
        </button>

        {uploadMessage && (
          <div className={`upload-status ${uploadMessage.type}`}>
            {uploadMessage.type === 'success' ? <CheckCircle size={14} /> : <AlertCircle size={14} />}
            <span>{uploadMessage.text}</span>
          </div>
        )}
      </div>
    </aside>
  );
};

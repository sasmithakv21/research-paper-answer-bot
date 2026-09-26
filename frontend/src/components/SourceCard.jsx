import React, { useState } from 'react';
import { FileText, ChevronDown, ChevronUp } from 'lucide-react';

export const SourceCard = ({ source }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="source-card">
      <div 
        className="source-header"
        onClick={() => setExpanded(!expanded)}
      >
        <FileText size={16} className="source-icon" />
        <span className="source-title">{source.paper}</span>
        <span className="source-page">Page {source.page}</span>
        {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </div>
      
      {expanded && (
        <div className="source-snippet">
          <p>"{source.snippet}"</p>
        </div>
      )}
    </div>
  );
};

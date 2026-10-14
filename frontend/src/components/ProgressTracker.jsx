import React from 'react';
import { Check, Loader2 } from 'lucide-react';

export default function ProgressTracker({ currentStep }) {
  // Steps: 1: Ingestion, 2: Master Analysis, 3: Audience Panel, 4: Shorts Clips
  const steps = [
    { num: 1, label: 'Video Ingestion' },
    { num: 2, label: 'Master Analysis & Rubrics' },
    { num: 3, label: 'Simulated Audience Panel' },
    { num: 4, label: 'Shorts & Insights' },
  ];

  return (
    <div className="progress-tracker">
      {steps.map((s) => {
        const isCompleted = currentStep > s.num;
        const isActive = currentStep === s.num;

        return (
          <div
            key={s.num}
            className={`step-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}
          >
            <div className="step-number">
              {isCompleted ? (
                <Check size={14} strokeWidth={3} />
              ) : isActive ? (
                <Loader2 size={14} className="spin-animation" />
              ) : (
                s.num
              )}
            </div>
            <span className="step-title">{s.label}</span>
          </div>
        );
      })}
    </div>
  );
}

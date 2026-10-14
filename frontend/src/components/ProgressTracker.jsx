import React from 'react';
import { Check, Sparkles, Brain, Users, Video } from 'lucide-react';

export default function ProgressTracker({ currentStep }) {
  // Steps: 1: Ingestion, 2: Master Analysis & Rubrics, 3: Simulated Audience Panel
  const steps = [
    {
      num: 1,
      label: 'Video Ingestion',
      icon: Video,
      description: 'Parsing YouTube video stream and preparing context window...',
    },
    {
      num: 2,
      label: 'Master Video Analysis',
      icon: Brain,
      description: 'Evaluating 4 Hook dimensions, generating titles, and computing readiness score with Gemini 3.8 Flash...',
    },
    {
      num: 3,
      label: 'Simulated Audience Panel',
      icon: Users,
      description: 'Simulating 3 category-specific audience personas & mapping disagreements matrix...',
    },
  ];

  const activeStepObj = steps.find((s) => s.num === currentStep) || steps[0];
  const progressPercent = Math.min(100, Math.round(((currentStep - 1) / steps.length) * 100) + 15);

  return (
    <div className="circular-loader-card">
      {/* Animated Glowing Circular Spinner */}
      <div className="spinner-ring-wrapper">
        <svg className="spinner-svg" viewBox="0 0 50 50">
          <circle
            className="spinner-circle-bg"
            cx="25"
            cy="25"
            r="20"
            fill="none"
            strokeWidth="4"
          />
          <circle
            className="spinner-circle-val"
            cx="25"
            cy="25"
            r="20"
            fill="none"
            strokeWidth="4"
            strokeDasharray="125"
            strokeDashoffset={125 - (125 * progressPercent) / 100}
          />
        </svg>
        <div className="spinner-center-icon">
          <span>🧠</span>
        </div>
      </div>

      <div className="loading-step-msg">
        Step {currentStep} of {steps.length}: {activeStepObj.label}
      </div>

      <p className="loading-subtext">
        {activeStepObj.description}
      </p>

      {/* Step Pills */}
      <div className="progress-tracker" style={{ margin: 0, width: '100%', maxWidth: '650px' }}>
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
                  <div
                    style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      background: 'currentColor',
                      animation: 'pulse-ring 1s infinite',
                    }}
                  />
                ) : (
                  s.num
                )}
              </div>
              <span className="step-title">{s.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

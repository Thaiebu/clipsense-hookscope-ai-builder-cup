import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="section-card" style={{ borderColor: 'var(--rose)', textAlign: 'center', padding: '2rem' }}>
          <AlertTriangle size={32} color="var(--rose)" style={{ margin: '0 auto 0.75rem' }} />
          <h4 style={{ color: 'var(--rose)', marginBottom: '0.5rem' }}>
            {this.props.title || 'Component Error'}
          </h4>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            {this.state.error?.message || 'Something went wrong rendering this section.'}
          </p>
          <button
            type="button"
            className="btn btn-outline btn-sm"
            onClick={this.handleRetry}
          >
            <RefreshCw size={12} />
            <span>Try Again</span>
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

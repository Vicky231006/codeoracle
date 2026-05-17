/**
 * App component tests
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
    expect(document.body).toBeTruthy();
  });

  it('renders header component', () => {
    render(<App />);
    const header = screen.getByText(/CodeOracle/i);
    expect(header).toBeInTheDocument();
  });
});

// Made with Bob

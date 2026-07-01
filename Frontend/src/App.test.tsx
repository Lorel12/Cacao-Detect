// @ts-nocheck
/// <reference types="jest" />

import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders the CacaoDetect experience', () => {
    render(<App />);
    expect(screen.getByText(/CacaoDetect/i)).toBeInTheDocument();
  });
});

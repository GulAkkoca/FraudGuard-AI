import React, { useState } from 'react';
import Dashboard from "./pages/Dashboard.jsx";
import LandingPage from "./pages/LandingPage.jsx";
import FAQPage from "./pages/FAQPage.jsx";

export default function App() {
  const [currentView, setCurrentView] = useState('landing');
  const [initialUrl, setInitialUrl] = useState('');

  if (currentView === 'landing') {
    return (
      <LandingPage 
        onEnterApp={(url) => {
          setInitialUrl(url || '');
          setCurrentView('dashboard');
        }} 
        onGoToFAQ={() => setCurrentView('faq')}
      />
    );
  }

  if (currentView === 'faq') {
    return (
      <FAQPage 
        onBackToLanding={() => setCurrentView('landing')} 
        onEnterApp={(url) => {
          setInitialUrl(url || '');
          setCurrentView('dashboard');
        }}
      />
    );
  }

  return (
    <Dashboard 
      onBack={() => {
        setInitialUrl('');
        setCurrentView('landing');
      }} 
      initialUrl={initialUrl}
    />
  );
}

import { useState, useEffect } from 'react';
import './SmartBanner.css';

export function SmartBanner() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Basic mobile detection
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent
    );
    
    // Only show if it's mobile and hasn't been closed in this session
    const isDismissed = sessionStorage.getItem('smart_banner_dismissed') === 'true';
    
    if (isMobile && !isDismissed) {
      setIsVisible(true);
    }
  }, []);

  const handleDismiss = () => {
    setIsVisible(false);
    sessionStorage.setItem('smart_banner_dismissed', 'true');
  };

  if (!isVisible) return null;

  // Em um cenário real, este link apontará para o GitHub Releases ou para o arquivo local
  const downloadLink = "https://github.com/LordWalace/Nexo/releases/latest";

  return (
    <div className="smart-banner">
      <div className="smart-banner-content">
        <div className="smart-banner-icon">
          <img src="/vite.svg" alt="App Icon" />
        </div>
        <div className="smart-banner-text">
          <strong>Nexo App</strong>
          <span>A experiência é melhor no app!</span>
        </div>
      </div>
      <div className="smart-banner-actions">
        <a href={downloadLink} className="smart-banner-download-btn">
          Baixar APK
        </a>
        <button onClick={handleDismiss} className="smart-banner-close-btn" aria-label="Fechar">
          &times;
        </button>
      </div>
    </div>
  );
}

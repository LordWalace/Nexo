import './App.css';

function App() {
  const downloadLink = "https://github.com/LordWalace/Nexo/releases/latest";
  const webAppLink = "https://app.nexo.com"; // Placeholder para a URL da versão Web (o app mobile compilado)

  return (
    <div className="landing-container">
      <svg width="0" height="0" style={{ position: 'absolute' }}>
        <defs>
          <linearGradient id="icon-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#a855f7" />
            <stop offset="100%" stopColor="#6366f1" />
          </linearGradient>
        </defs>
      </svg>
      <nav className="navbar">
        <div className="nav-logo">
          <div className="logo-icon"></div>
          <span>Nexo</span>
        </div>
        <div className="nav-links">
          <a href="#features">Recursos</a>
          <a href="#about">Sobre</a>
          <a href={webAppLink} className="nav-btn-outline">Acessar Web</a>
        </div>
      </nav>

      <main className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">O seu diário de estudos <span>definitivo</span>.</h1>
          <p className="hero-subtitle">
            Organize suas matérias, acompanhe seu progresso e alcance suas metas com o Nexo.
            Disponível para Android e Web.
          </p>
          <div className="hero-actions">
            <a href={downloadLink} className="btn-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
              Baixar para Android (APK)
            </a>
            <a href={webAppLink} className="btn-secondary">
              Abrir no Navegador
            </a>
          </div>
        </div>
        <div className="hero-visual">
          <div className="mockup-glass">
            <div className="mockup-content">
              <h3>Progresso Semanal</h3>
              <div className="progress-bar-container">
                <div className="progress-bar" style={{ width: '75%' }}></div>
              </div>
              <ul className="mockup-list">
                <li><span className="dot math"></span> Matemática: 12h</li>
                <li><span className="dot history"></span> História: 8h</li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      <section id="features" className="features-section">
        <h2>Por que escolher o Nexo?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
            </div>
            <h3>Métricas Precisas</h3>
            <p>Visualize seu desempenho com gráficos detalhados e saiba exatamente onde focar.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"></path></svg>
            </div>
            <h3>Sincronização Nuvem</h3>
            <p>Seus dados seguros no seu próprio Google Drive. Acesse de qualquer dispositivo.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
            </div>
            <h3>Foco Total</h3>
            <p>Uma interface limpa e imersiva para que você se concentre apenas no que importa: estudar.</p>
          </div>
        </div>
      </section>
      
      <footer className="footer">
        <p>&copy; 2026 Nexo. Construído para estudantes.</p>
      </footer>
    </div>
  );
}

export default App;

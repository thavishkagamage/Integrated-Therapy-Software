import React from 'react';
import '../app/App.css';

function Team() {
  return (
    <div className="team-page">
      {/* HERO SECTION */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Meet the TheraThrive Team</h1>
          <p className="hero-subtitle">
            A cross-disciplinary group passionate about transforming mental health care through technology and human connection.
          </p>
        </div>
        <div className="hero-image">
          <img 
            src="/TheraThrive1.png" 
            alt="TheraThrive Logo" 
          />
        </div>
        <div className="wave-divider-bottom">
          <svg
            viewBox="0 0 1200 120"
            preserveAspectRatio="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M321.39,56.39C236.14,65.49,153,85,68.07,85
                 c-33.06,0-66.45-3.22-98.07-9.54V120H1200V0
                 C1126.67,26.51,1032.51,57,927.87,57
                 C813.5,57,744.44,3,633.74,3
                 C540.72,3,449.18,47.8,321.39,56.39Z"
              fill="var(--primary-bg)"
            />
          </svg>
        </div>
      </section>

      {/* TEAM SECTION */}
      <main className="main-sections">
        <section className="card-section">
          <h2 className="section-title">Our Team</h2>
          <p className="section-content">
            TheraThrive is powered by a diverse team of engineers and developers committed to building
            empathetic, effective mental health solutions through collaboration, creativity, and care.
          </p>
          <ul className="section-content list">
            <li><strong>Alex Gribble (BME):</strong> Biomedical insights and user empathy</li>
            <li><strong>Grant Guernsey (CS):</strong> Full-stack developer and architecture lead</li>
            <li><strong>Ricky Roberts (CS):</strong> AI integration and backend systems</li>
            <li><strong>Kyle Woods (EET):</strong> Hardware integration and support systems</li>
            <li><strong>Thavishka Gamage (CS):</strong> UI/UX design and frontend development</li>
          </ul>
        </section>
      </main>

    </div>
  );
}

export default Team;

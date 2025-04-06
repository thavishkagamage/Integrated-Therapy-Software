import React from 'react';
import { Link } from 'react-router-dom';
import '../app/App.css';  // Make sure this is the correct path to your CSS file

function Home() {
  return (
    <div className="home-page">

      {/* HERO SECTION */}
      <section className="hero-section">
        {/* Left Column: Hero Text */}
        <div className="hero-content">
          <h1 className="hero-title">
            TheraThrive Integrated Therapy Software
          </h1>
          <p className="hero-subtitle">
            Combining computerized CBT with social support for holistic treatment of depression.
          </p>
          <p className="hero-subtitle">
            Get immediate, affordable, and always-available therapy support through AI-driven sessions.
          </p>
          <button className="hero-button">Get Started</button>
        </div>

        {/* Right Column: Hero Image */}
        <div className="hero-image">
          <img 
            src="/TheraThrive1.png" 
            alt="TheraThrive Logo" 
          />
        </div>

        {/* Wave Divider (Bottom) */}
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

      <main className="main-sections">

        {/* GET STARTED */}
        <section className="card-section">
          <h2 className="section-title">Getting Started</h2>
          <p className="section-content">
            Follow these steps to begin using TheraThrive:
          </p>
          <ul className="section-content list">
            <li>
              Navigate to the <Link to="/login" className="link-button">Login</Link> page and click <strong>Sign Up</strong>.
            </li>
            <li>Create an account using a unique username, email, and password.</li>
            <li>
              Once logged in, access the 
              <Link to="/chatbot" className="link-button"> Chat</Link>, 
              <Link to="/conversations" className="link-button"> Conversations</Link>, and 
              <Link to="/goals" className="link-button"> Goals</Link> pages from your dashboard.
            </li>
          </ul>
        </section>

        {/* FIRST SESSION */}
        <section className="card-section">
          <h2 className="section-title">Start Your First Session</h2>
          <p className="section-content">
            Jump into your first CBT session with our AI therapeutic assistant:
          </p>
          <ul className="section-content list">
            <li>Go to the <Link to="/chatbot" className="link-button">Chat</Link> page.</li>
            <li>Click on <strong>Session 1</strong> to begin.</li>
            <li>Type your message into the chat box and click <strong>Send</strong>.</li>
            <li>Follow the prompts to progress through your first CBT experience.</li>
          </ul>
        </section>

        {/* PAST CONVERSATIONS */}
        <section className="card-section">
          <h2 className="section-title">Review Past Conversations</h2>
          <p className="section-content">
            Your session history is always available for review:
          </p>
          <ul className="section-content list">
            <li>Visit the <Link to="/conversations" className="link-button">Conversations</Link> page.</li>
            <li>View previous chats, delete old sessions, or pick up where you left off.</li>
          </ul>
        </section>

        {/* CBT EXPLAINER */}
        <section className="card-section">
          <h2 className="section-title">What is CBT?</h2>
          <p className="section-content">
            Cognitive Behavioral Therapy (CBT) is a practical, results-focused form of therapy that aims to improve mental well-being
            by addressing the connections between thoughts, emotions, and behaviors.
          </p>
          <p className="section-content">
            It empowers individuals to identify and challenge negative thought patterns, and replace them with healthier alternatives—using structured, goal-oriented techniques proven to reduce symptoms of depression and anxiety.
          </p>
        </section>

      </main>
    </div>
  );
}

export default Home;

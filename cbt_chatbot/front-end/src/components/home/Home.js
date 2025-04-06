import React from 'react';
import '../app/App.css';

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

      {/* MAIN CONTENT */}
      <main className="main-sections">

        {/* TREATMENT GAP */}
        <section className="card-section">
          <h2 className="section-title">Treatment Gap</h2>
          <p className="section-content">
            The rising demand for mental health care has outpaced the supply of professionals.
            Digital, software-based Cognitive Behavioral Therapy (CBT) solutions have emerged to fill this gap
            by offering affordable, always-available support. However, they often lack the real-life connections
            crucial for overcoming depression—highlighting the need for an integrated approach that combines
            CBT with social support and accountability.
          </p>
        </section>

        {/* WHAT IS CBT? & TARGET USER (Side by Side) */}
        <div className="card-grid">
          <section className="card-section">
            <h2 className="section-title">What is CBT?</h2>
            <p className="section-content">
              Cognitive Behavioral Therapy (CBT) is a structured, goal-oriented approach that focuses on the present
              to change negative thought patterns and behaviors. It works by helping therapists and clients identify,
              challenge, and replace negative automatic thoughts through strategic growth experiences.
            </p>
          </section>
          <section className="card-section">
            <h2 className="section-title">Target User</h2>
            <ul className="section-content list">
              <li>Individuals with Major Depressive Disorder (may not have a formal diagnosis)</li>
              <li>Technology proficient—using smartphones or laptops</li>
              <li>Often disconnected from supportive social relationships</li>
              <li>Quiet, isolated environment at home</li>
              <li>Ages 12 to 49 years old</li>
            </ul>
          </section>
        </div>

        {/* OUR SOLUTION */}
        <section className="card-section">
          <h2 className="section-title">Our Solution</h2>
          <p className="section-content">
            TheraThrive integrates computerized CBT with relationship-building support. Users log in to our
            convenient website to chat with an AI-powered assistant for weekly hour-long therapy sessions.
            The chatbot leverages a structured agenda, agenda-specific prompts, and specialized tools to deliver
            effective therapy and foster social accountability.
          </p>
        </section>

        {/* TECHNOLOGY & MARKET OPPORTUNITY (Side by Side) */}
        <div className="card-grid">
          <section className="card-section">
            <h2 className="section-title">Technology Used</h2>
            <ul className="section-content list">
              <li><strong>Django:</strong> Python back-end framework for API requests</li>
              <li><strong>React:</strong> Dynamic front-end in JavaScript</li>
              <li><strong>Postgres:</strong> Reliable database for user data</li>
              <li><strong>RESTful API:</strong> Seamless front-end/back-end communication</li>
              <li><strong>OpenAI:</strong> Advanced LLMs powering the virtual therapist</li>
            </ul>
          </section>
          <section className="card-section">
            <h2 className="section-title">Market Opportunity</h2>
            <p className="section-content">
              The U.S. mental health apps market was valued at $6.25 billion in 2023 and is growing at an annual rate of
              15.2%. With an estimated API usage cost of just $0.015 per 1-hour conversation, TheraThrive is positioned
              for rapid adoption and scalability.
            </p>
            <p className="section-content">
              Our competitive differentiator: combining CBT with relationship-building support for holistic psychological
              and social treatment of depression.
            </p>
          </section>
        </div>

        {/* CHALLENGES & FUTURE IMPROVEMENTS (Side by Side) */}
        <section className="card-section">
          <h2 className="section-title">Challenges &amp; Future Improvements</h2>
          <div className="card-grid">
            <div>
              <h3 className="sub-title">Challenges Faced</h3>
              <ul className="section-content list">
                <li>Tool call misfires (agenda item completion issues)</li>
                <li>Cross-disciplinary collaboration complexities</li>
                <li>Prompt engineering to guide AI behavior effectively</li>
              </ul>
            </div>
            <div>
              <h3 className="sub-title">Future Improvements</h3>
              <ul className="section-content list">
                <li>Co-creation of conversation agendas with users &amp; chatbot</li>
                <li>Negative Automatic Thoughts journal feature</li>
                <li>Time-elapsed prompt input for smoother conversation flow</li>
                <li>Accountability partner messaging</li>
              </ul>
            </div>
          </div>
        </section>

        {/* TEAM */}
        <section className="card-section">
          <h2 className="section-title">Meet the Team</h2>
          <ul className="section-content list">
            <li>Alex Gribble (BME)</li>
            <li>Grant Guernsey (CS)</li>
            <li>Ricky Roberts (CS)</li>
            <li>Kyle Woods (EET)</li>
            <li>Thavishka Gamage (CS)</li>
          </ul>
        </section>
      </main>
    </div>
  );
}

export default Home;

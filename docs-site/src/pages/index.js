import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroLogoContainer}>
          <img
            src="/img/logo.svg"
            alt="Physical AI Book Logo"
            className={styles.heroLogo}
          />
        </div>
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Read the Textbook
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome`}
      description="Introduction to the Physical AI Book - An Interactive Textbook for Robotics and AI">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <h2>Physical AI Fundamentals</h2>
                <p>Learn about the foundations of embodied intelligence and how AI interacts with the real world.</p>
              </div>
              <div className="col col--4">
                <h2>Humanoid Robotics</h2>
                <p>Explore the principles of humanoid robotics including kinematics, control, and locomotion.</p>
              </div>
              <div className="col col--4">
                <h2>ROS2 and Simulation</h2>
                <p>Master ROS2 fundamentals and digital twin technologies for robotics development.</p>
              </div>
            </div>
          </div>
        </section>
        
        {/* Include the intro content */}
        <section className="container padding-horiz--md">
          <div className="row">
            <div className="col">
              <h2>What You'll Learn</h2>
              <ul>
                <li>The fundamentals of physical AI and embodied intelligence</li>
                <li>Humanoid robotics basics including kinematics and control</li>
                <li>ROS2 fundamentals for robotics development</li>
                <li>Digital twins and simulation environments</li>
                <li>Vision-Language-Action systems</li>
                <li>A capstone project integrating all concepts</li>
              </ul>
              
              <h2>How to Use This Book</h2>
              <p>This interactive textbook allows you to:</p>
              <ol>
                <li>Read through the structured content</li>
                <li>Ask questions about the content using the AI assistant</li>
                <li>Select text and ask for clarification directly</li>
                <li>Search across all chapters for specific topics</li>
              </ol>
              
              <p>Let's begin our journey into the fascinating world of physical AI!</p>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
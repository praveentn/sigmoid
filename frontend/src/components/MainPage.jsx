import { useEffect, useState } from 'react'
import { api } from '../api/client'
import Header from './layout/Header'
import Footer from './layout/Footer'
import Hero from './sections/Hero'
import Impact from './sections/Impact'
import About from './sections/About'
import Experience from './sections/Experience'
import Skills from './sections/Skills'
import Projects from './sections/Projects'
import Education from './sections/Education'
import Certifications from './sections/Certifications'
import Research from './sections/Research'

export default function MainPage() {
  const [data, setData] = useState({
    profile: null,
    experience: [],
    education: [],
    skills: [],
    certifications: [],
    projects: [],
    research: [],
    awards: [],
    impact: [],
    loading: true,
  })

  useEffect(() => {
    Promise.all([
      api.getProfile(),
      api.getExperience(),
      api.getEducation(),
      api.getSkills(),
      api.getCertifications(),
      api.getProjects(),
      api.getResearch(),
      api.getAwards(),
      api.getImpact(),
    ]).then(([profile, experience, education, skills, certifications, projects, research, awards, impact]) => {
      setData({
        profile: profile.data,
        experience: experience.data,
        education: education.data,
        skills: skills.data,
        certifications: certifications.data,
        projects: projects.data,
        research: research.data,
        awards: awards.data,
        impact: impact.data,
        loading: false,
      })
    }).catch(() => setData(d => ({ ...d, loading: false })))
  }, [])

  // Scroll animation observer
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => entries.forEach(e => e.isIntersecting && e.target.classList.add('visible')),
      { threshold: 0.08 }
    )
    document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el))
    return () => observer.disconnect()
  }, [data.loading])

  if (data.loading) {
    return (
      <div className="min-h-screen bg-snow flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-6 h-6 border-2 border-cloud border-t-ink rounded-full animate-spin" />
          <span className="text-xs font-mono text-silver tracking-widest">LOADING</span>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-snow">
      <Header profile={data.profile} />
      <main>
        <Hero profile={data.profile} />
        <Impact metrics={data.impact} />
        <About profile={data.profile} awards={data.awards} />
        <Experience items={data.experience} />
        <Skills items={data.skills} />
        <Projects items={data.projects} />
        <Education items={data.education} certifications={data.certifications} />
        <Research items={data.research} />
      </main>
      <Footer profile={data.profile} />
    </div>
  )
}

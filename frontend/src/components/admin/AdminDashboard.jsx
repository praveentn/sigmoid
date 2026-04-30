import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import ProfileEditor from './editors/ProfileEditor'
import ExperienceEditor from './editors/ExperienceEditor'
import EducationEditor from './editors/EducationEditor'
import SkillsEditor from './editors/SkillsEditor'
import CertificationsEditor from './editors/CertificationsEditor'
import ProjectsEditor from './editors/ProjectsEditor'
import ResearchEditor from './editors/ResearchEditor'
import AwardsEditor from './editors/AwardsEditor'
import ImpactEditor from './editors/ImpactEditor'

const SECTIONS = [
  { key: 'profile', label: 'Profile', icon: '◆' },
  { key: 'impact', label: 'Impact Metrics', icon: '◈' },
  { key: 'experience', label: 'Experience', icon: '◇' },
  { key: 'education', label: 'Education', icon: '◉' },
  { key: 'skills', label: 'Skills', icon: '◎' },
  { key: 'certifications', label: 'Certifications', icon: '◐' },
  { key: 'projects', label: 'Projects', icon: '◑' },
  { key: 'research', label: 'Research', icon: '◒' },
  { key: 'awards', label: 'Awards', icon: '★' },
]

const EDITORS = {
  profile: ProfileEditor,
  impact: ImpactEditor,
  experience: ExperienceEditor,
  education: EducationEditor,
  skills: SkillsEditor,
  certifications: CertificationsEditor,
  projects: ProjectsEditor,
  research: ResearchEditor,
  awards: AwardsEditor,
}

export default function AdminDashboard() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [activeSection, setActiveSection] = useState('profile')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const handleLogout = () => {
    logout()
    navigate('/admin')
  }

  const ActiveEditor = EDITORS[activeSection]

  return (
    <div className="min-h-screen bg-ink-soft flex">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-56' : 'w-14'} bg-ink flex flex-col transition-all duration-200 shrink-0`}>
        {/* Logo */}
        <div className="px-4 py-5 border-b border-ink-muted flex items-center justify-between">
          {sidebarOpen && (
            <div>
              <p className="text-xs font-bold text-snow tracking-wide">Portfolio CMS</p>
              <p className="text-xs text-snow/30 font-mono">{user?.username}</p>
            </div>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-snow/40 hover:text-snow transition-colors p-1"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M1 7H13M1 3H13M1 11H13" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
            </svg>
          </button>
        </div>

        {/* Nav */}
        <nav className="flex-1 py-4">
          {SECTIONS.map(section => (
            <button
              key={section.key}
              onClick={() => setActiveSection(section.key)}
              className={`admin-sidebar-link w-full ${activeSection === section.key ? 'active' : ''}`}
            >
              <span className="shrink-0 text-sm">{section.icon}</span>
              {sidebarOpen && <span className="text-xs tracking-wide">{section.label}</span>}
            </button>
          ))}
        </nav>

        {/* Footer actions */}
        <div className="border-t border-ink-muted">
          {sidebarOpen && (
            <a
              href="/"
              target="_blank"
              rel="noopener noreferrer"
              className="admin-sidebar-link w-full"
            >
              <span className="shrink-0 text-sm">↗</span>
              <span className="text-xs tracking-wide">View Site</span>
            </a>
          )}
          <button onClick={handleLogout} className="admin-sidebar-link w-full text-left">
            <span className="shrink-0 text-sm">→</span>
            {sidebarOpen && <span className="text-xs tracking-wide">Sign Out</span>}
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        {/* Top bar */}
        <div className="bg-ink-soft border-b border-ink-muted px-8 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-sm font-bold text-snow tracking-wide">
              {SECTIONS.find(s => s.key === activeSection)?.label}
            </h1>
            <p className="text-xs text-snow/30 font-mono mt-0.5">Editing live data</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-green-400" />
            <span className="text-xs font-mono text-snow/40">Connected</span>
          </div>
        </div>

        {/* Editor */}
        <div className="p-8">
          {ActiveEditor && <ActiveEditor />}
        </div>
      </main>
    </div>
  )
}

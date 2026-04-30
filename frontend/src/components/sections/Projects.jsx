import { useState } from 'react'

const CATEGORIES = ['All', 'Agentic AI', 'RAG', 'ML/DL', 'ML/NLP', 'GenAI Platform', 'Accessibility AI']

function ProjectCard({ project, i }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div
      className="animate-on-scroll border border-cloud bg-white hover:border-mist transition-all duration-200 flex flex-col"
      style={{ animationDelay: `${i * 0.06}s` }}
    >
      <div className="p-6 flex-1">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-mono text-silver">{project.category}</span>
            {project.is_featured && (
              <span className="text-xs font-mono bg-ink text-snow px-2 py-0.5">FEATURED</span>
            )}
          </div>
          <span className="text-xs font-mono text-mist shrink-0">{project.period}</span>
        </div>

        <h3 className="font-bold text-ink text-base leading-snug mb-1">{project.name}</h3>
        <p className="text-xs text-silver mb-3">{project.company} · {project.role}</p>

        <p className="text-sm text-graphite leading-relaxed mb-4">{project.description}</p>

        {/* Tech stack */}
        {project.tech_stack?.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {project.tech_stack.map(t => (
              <span key={t} className="text-xs font-mono px-2 py-0.5 bg-fog text-graphite border border-cloud">{t}</span>
            ))}
          </div>
        )}

        {/* Highlights toggle */}
        {project.highlights?.length > 0 && (
          <>
            <button
              onClick={() => setExpanded(!expanded)}
              className="text-xs font-mono text-silver hover:text-ink transition-colors flex items-center gap-1"
            >
              {expanded ? 'Less' : 'Key highlights'}
              <svg width="10" height="10" viewBox="0 0 10 10" fill="none" className={`transition-transform ${expanded ? 'rotate-180' : ''}`}>
                <path d="M2 4L5 7L8 4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
              </svg>
            </button>
            {expanded && (
              <ul className="mt-3 space-y-1.5">
                {project.highlights.map((h, i) => (
                  <li key={i} className="flex gap-2 text-xs text-graphite">
                    <span className="text-mist shrink-0">—</span>
                    {h}
                  </li>
                ))}
              </ul>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default function Projects({ items }) {
  const [activeCategory, setActiveCategory] = useState('All')

  if (!items?.length) return null

  const categories = ['All', ...new Set(items.map(p => p.category).filter(Boolean))]
  const filtered = activeCategory === 'All' ? items : items.filter(p => p.category === activeCategory)

  return (
    <section id="projects" className="py-24 bg-fog">
      <div className="section-container">
        <div className="animate-on-scroll mb-10">
          <p className="section-label">Selected Work</p>
          <h2 className="section-title mb-6">
            Enterprise AI <span className="text-silver">Solutions</span>
          </h2>
          {/* Category filter */}
          <div className="flex flex-wrap gap-2">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`text-xs font-mono px-3 py-1.5 border transition-colors ${
                  activeCategory === cat
                    ? 'bg-ink text-snow border-ink'
                    : 'border-cloud text-silver hover:border-ink hover:text-ink'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((project, i) => (
            <ProjectCard key={project.id} project={project} i={i} />
          ))}
        </div>
      </div>
    </section>
  )
}

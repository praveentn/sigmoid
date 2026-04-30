import { useState } from 'react'

function ExperienceCard({ item, index }) {
  const [expanded, setExpanded] = useState(index === 0)

  return (
    <div className="animate-on-scroll relative pl-8 pb-12 last:pb-0">
      {/* Timeline dot */}
      <div className={`absolute left-0 top-1.5 w-2 h-2 rounded-full border-2 ${item.is_current ? 'bg-ink border-ink' : 'bg-snow border-mist'}`} />

      {/* Card */}
      <div className={`border transition-colors duration-200 ${expanded ? 'border-cloud bg-white' : 'border-transparent hover:border-cloud'}`}>
        <button
          className="w-full text-left p-6 pb-5"
          onClick={() => setExpanded(!expanded)}
        >
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <div className="flex flex-wrap items-center gap-2 mb-1">
                <span className="text-xs font-mono text-silver">{item.period_start} — {item.period_end}</span>
                {item.is_current && (
                  <span className="text-xs font-mono bg-ink text-snow px-2 py-0.5">CURRENT</span>
                )}
              </div>
              <h3 className="text-lg font-bold text-ink tracking-tight leading-snug">{item.role}</h3>
              <p className="text-sm font-medium text-silver mt-0.5">{item.company}</p>
              {item.location && <p className="text-xs text-mist mt-0.5">{item.location}</p>}
            </div>
            <div className={`mt-1 transition-transform duration-200 ${expanded ? 'rotate-180' : ''}`}>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M4 6L8 10L12 6" stroke="#888" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
          </div>

          {item.tagline && (
            <p className="text-sm text-graphite/70 mt-3 leading-relaxed italic border-l-2 border-cloud pl-3">
              {item.tagline}
            </p>
          )}
        </button>

        {expanded && item.highlights?.length > 0 && (
          <div className="px-6 pb-6 border-t border-fog">
            <ul className="mt-4 space-y-3">
              {item.highlights.map((h, i) => (
                <li key={i} className="flex gap-3 text-sm text-graphite leading-relaxed">
                  <span className="text-mist mt-0.5 shrink-0">—</span>
                  <span>{h}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default function Experience({ items }) {
  if (!items?.length) return null

  return (
    <section id="experience" className="py-24 bg-fog">
      <div className="section-container">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-16">
          {/* Sticky heading */}
          <div className="lg:col-span-4">
            <div className="lg:sticky lg:top-24">
              <p className="section-label">Career</p>
              <h2 className="section-title mb-4">
                Professional<br />
                <span className="text-silver">Experience</span>
              </h2>
              <p className="text-sm text-graphite leading-relaxed mt-4">
                {items.length} roles across {new Set(items.flatMap(i => i.company.split(' | '))).size} organisations.
                16+ years from web engineering to enterprise AI architecture.
              </p>
              <div className="mt-8 flex flex-col gap-3">
                {items.map((item, i) => (
                  <a key={item.id} href="#" className="text-xs font-mono text-silver hover:text-ink transition-colors">
                    {item.period_start?.split(' ')[1]} · {item.company?.split(' ')[0]}
                  </a>
                ))}
              </div>
            </div>
          </div>

          {/* Timeline */}
          <div className="lg:col-span-8 relative">
            <div className="timeline-line" />
            {items.map((item, i) => (
              <ExperienceCard key={item.id} item={item} index={i} />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

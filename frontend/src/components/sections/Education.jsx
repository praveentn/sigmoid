export default function Education({ items, certifications }) {
  if (!items?.length) return null

  const featured = certifications?.filter(c => c.is_featured) || []
  const others = certifications?.filter(c => !c.is_featured) || []

  return (
    <section id="education" className="py-24 bg-snow">
      <div className="section-container">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-16">
          {/* Education */}
          <div className="lg:col-span-6 animate-on-scroll">
            <p className="section-label">Education</p>
            <h2 className="section-title mb-10">
              Academic <span className="text-silver">Background</span>
            </h2>
            <div className="space-y-0">
              {items.map((edu, i) => (
                <div key={edu.id} className="flex gap-6 py-6 border-b border-cloud last:border-0">
                  <div className="shrink-0 w-14 text-right">
                    <span className="text-xs font-mono font-bold text-ink">{edu.year}</span>
                  </div>
                  <div>
                    <h3 className="font-bold text-ink text-sm leading-snug">{edu.degree}</h3>
                    <p className="text-xs text-silver mt-0.5">{edu.institution}</p>
                    {edu.description && (
                      <p className="text-xs text-mist mt-1.5 leading-relaxed">{edu.description}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Certifications */}
          <div className="lg:col-span-6 animate-on-scroll" style={{ animationDelay: '0.1s' }}>
            <p className="section-label">Credentials</p>
            <h2 className="section-title mb-10">
              Certifications <span className="text-silver">& Badges</span>
            </h2>

            {/* Featured certs */}
            <div className="space-y-0 mb-6">
              {featured.map(cert => (
                <div key={cert.id} className="flex items-center justify-between py-4 border-b border-cloud">
                  <div>
                    <p className="text-sm font-semibold text-ink leading-snug">{cert.name}</p>
                    <p className="text-xs text-silver mt-0.5">{cert.issuer}</p>
                  </div>
                  <span className="text-xs font-mono text-mist shrink-0 ml-4">{cert.year}</span>
                </div>
              ))}
            </div>

            {/* Others */}
            {others.length > 0 && (
              <div className="space-y-0">
                {others.map(cert => (
                  <div key={cert.id} className="flex items-center justify-between py-3">
                    <p className="text-xs text-graphite">{cert.name} · {cert.issuer}</p>
                    <span className="text-xs font-mono text-mist ml-4">{cert.year}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}

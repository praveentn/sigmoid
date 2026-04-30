export default function Skills({ items }) {
  if (!items?.length) return null

  return (
    <section id="skills" className="py-24 bg-snow">
      <div className="section-container">
        <div className="animate-on-scroll mb-14">
          <p className="section-label">Capabilities</p>
          <h2 className="section-title">
            Technical <span className="text-silver">Expertise</span>
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-cloud">
          {items.map((skill, i) => (
            <div
              key={skill.id}
              className="bg-snow p-8 hover:bg-white transition-colors animate-on-scroll group"
              style={{ animationDelay: `${i * 0.05}s` }}
            >
              <div className="flex items-start justify-between mb-5">
                <h3 className="text-sm font-bold text-ink tracking-wide">{skill.category}</h3>
                <span className="text-xs font-mono text-mist">{String(i + 1).padStart(2, '0')}</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {skill.items?.map(tag => (
                  <span key={tag} className="tag">{tag}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

const TYPE_LABELS = {
  thesis: 'Thesis',
  publication: 'Publication',
  article: 'Article',
}

export default function Research({ items }) {
  if (!items?.length) return null

  return (
    <section id="research" className="py-24 bg-ink">
      <div className="section-container">
        <div className="animate-on-scroll mb-14">
          <p className="section-label text-snow/30">Intellectual Work</p>
          <h2 className="text-3xl md:text-4xl font-bold text-snow tracking-tight mb-4">
            Research & <span className="text-snow/40">Publications</span>
          </h2>
          <p className="text-sm text-snow/40 max-w-xl leading-relaxed">
            Spanning quantum cryptography, computer vision, and evolutionary computation.
            Patent holder. Contributing to the frontier of applied AI research.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-ink-muted">
          {items.map((item, i) => (
            <div
              key={item.id}
              className="bg-ink-soft p-8 hover:bg-ink-mid transition-colors animate-on-scroll"
              style={{ animationDelay: `${i * 0.08}s` }}
            >
              <div className="flex items-center gap-3 mb-4">
                <span className="text-xs font-mono text-snow/30 border border-snow/10 px-2 py-0.5">
                  {TYPE_LABELS[item.type] || item.type}
                </span>
                {item.focus_area && (
                  <span className="text-xs font-mono text-snow/20">{item.focus_area}</span>
                )}
              </div>
              <h3 className="text-base font-semibold text-snow leading-snug mb-3">{item.title}</h3>
              <p className="text-sm text-snow/40 leading-relaxed">{item.description}</p>
            </div>
          ))}
        </div>

        {/* Patent note */}
        <div className="animate-on-scroll mt-12 flex items-center gap-4 py-6 border-t border-ink-muted">
          <div className="w-px h-12 bg-snow/10" />
          <div>
            <p className="text-xs font-mono text-snow/30 uppercase tracking-widest mb-1">IP & Innovation</p>
            <p className="text-sm text-snow/50">Patent holder. Active contributor to AI research and thought leadership at Ernst & Young and beyond.</p>
          </div>
        </div>
      </div>
    </section>
  )
}

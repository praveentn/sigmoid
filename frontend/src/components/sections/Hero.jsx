export default function Hero({ profile }) {
  if (!profile) return null

  return (
    <section className="relative min-h-screen bg-ink flex flex-col justify-center overflow-hidden">
      {/* Subtle grid pattern */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: 'linear-gradient(#ffffff 1px, transparent 1px), linear-gradient(90deg, #ffffff 1px, transparent 1px)',
          backgroundSize: '80px 80px',
        }}
      />

      {/* Content */}
      <div className="relative section-container pt-32 pb-24">
        {/* Pre-label */}
        <div className="flex items-center gap-3 mb-8 animate-fade-in">
          <div className="w-8 h-px bg-snow/30" />
          <span className="text-xs font-mono tracking-[0.3em] uppercase text-snow/40">
            {profile.company} — {profile.location}
          </span>
        </div>

        {/* Name */}
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-black text-snow leading-none tracking-tighter mb-6">
          {profile.name?.split(' ').map((word, i) => (
            <span key={i} className="block">{word}</span>
          ))}
        </h1>

        {/* Title */}
        <div className="flex items-center gap-4 mb-8">
          <div className="w-12 h-px bg-snow/20" />
          <p className="text-sm md:text-base font-medium text-snow/60 tracking-wide">
            {profile.title}
          </p>
        </div>

        {/* Tagline */}
        <p className="max-w-2xl text-lg md:text-xl text-snow/40 leading-relaxed font-light mb-12">
          {profile.tagline}
        </p>

        {/* CTA row */}
        <div className="flex flex-wrap items-center gap-4">
          {profile.linkedin_url && (
            <a
              href={profile.linkedin_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-snow text-ink px-6 py-3 text-sm font-semibold tracking-wide hover:bg-cloud transition-colors"
            >
              LinkedIn Profile
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <path d="M1 11L11 1M11 1H4M11 1V8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </a>
          )}
          <a
            href="#experience"
            className="inline-flex items-center gap-2 border border-snow/30 text-snow/70 px-6 py-3 text-sm font-medium tracking-wide hover:border-snow hover:text-snow transition-colors"
          >
            View Career
          </a>
          {profile.email && (
            <a
              href={`mailto:${profile.email}`}
              className="text-sm font-mono text-snow/40 hover:text-snow/70 transition-colors"
            >
              {profile.email}
            </a>
          )}
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-12 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 opacity-30">
          <span className="text-xs font-mono text-snow tracking-widest">SCROLL</span>
          <div className="w-px h-12 bg-gradient-to-b from-snow to-transparent" />
        </div>
      </div>

      {/* Bottom gradient */}
      <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-snow to-transparent" />
    </section>
  )
}

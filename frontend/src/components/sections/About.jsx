export default function About({ profile, awards }) {
  if (!profile) return null

  const paragraphs = profile.bio?.split('\n\n').filter(Boolean) || []

  return (
    <section id="about" className="py-24 bg-snow">
      <div className="section-container">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-16">
          {/* Left: bio */}
          <div className="lg:col-span-7 animate-on-scroll">
            <p className="section-label">About</p>
            <h2 className="section-title mb-8">
              AI architect.<br />
              <span className="text-silver">Practice builder.</span>
            </h2>
            <div className="space-y-5">
              {paragraphs.map((p, i) => (
                <p key={i} className="text-base text-graphite leading-relaxed">
                  {p}
                </p>
              ))}
            </div>

            {/* Quick links */}
            <div className="flex flex-wrap gap-4 mt-10">
              {profile.linkedin_url && (
                <a href={profile.linkedin_url} target="_blank" rel="noopener noreferrer" className="btn-secondary text-xs">
                  LinkedIn
                </a>
              )}
              {profile.credly_url && (
                <a href={profile.credly_url} target="_blank" rel="noopener noreferrer" className="btn-secondary text-xs">
                  Credly Badges
                </a>
              )}
              {profile.email && (
                <a href={`mailto:${profile.email}`} className="btn-ghost text-xs">
                  {profile.email}
                </a>
              )}
            </div>
          </div>

          {/* Right: identity card */}
          <div className="lg:col-span-5 animate-on-scroll" style={{ animationDelay: '0.15s' }}>
            {/* Profile card */}
            <div className="border border-cloud bg-white p-8 mb-6">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h3 className="font-bold text-ink text-xl tracking-tight">{profile.name}</h3>
                  <p className="text-sm text-silver mt-0.5">{profile.company}</p>
                </div>
                <div className="w-14 h-14 bg-ink flex items-center justify-center">
                  <span className="text-snow font-black text-xl">
                    {profile.name?.split(' ').map(w => w[0]).join('').slice(0, 2)}
                  </span>
                </div>
              </div>

              <div className="space-y-3 border-t border-cloud pt-6">
                {[
                  { label: 'Location', value: profile.location },
                  { label: 'Phone', value: profile.phone },
                  { label: 'Experience', value: `${profile.years_experience}+ years` },
                  { label: 'Solutions Delivered', value: `${profile.solutions_delivered}+ enterprise AI` },
                  { label: 'Travel', value: profile.visa_info },
                ].map(({ label, value }) => value && (
                  <div key={label} className="flex items-start justify-between gap-4">
                    <span className="text-xs font-mono text-silver uppercase tracking-wide shrink-0">{label}</span>
                    <span className="text-xs text-graphite text-right">{value}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Awards */}
            {awards?.length > 0 && (
              <div className="space-y-3">
                <p className="text-xs font-mono tracking-[0.2em] uppercase text-silver">Recognition</p>
                {awards.map(award => (
                  <div key={award.id} className="flex gap-4 py-3 border-b border-cloud last:border-0">
                    <div className="w-1 h-1 rounded-full bg-ink mt-2 shrink-0" />
                    <div>
                      <p className="text-sm font-semibold text-ink">{award.title}</p>
                      <p className="text-xs text-silver mt-0.5">{award.organization} · {award.year}</p>
                    </div>
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

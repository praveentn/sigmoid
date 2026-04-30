export default function Footer({ profile }) {
  return (
    <footer className="bg-ink text-snow/60 py-16 mt-0">
      <div className="max-w-6xl mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
          {/* Identity */}
          <div>
            <h3 className="font-bold text-snow text-lg mb-1">{profile?.name || 'Praveen T N'}</h3>
            <p className="text-sm text-snow/50 mb-4">{profile?.title}</p>
            <p className="text-xs text-snow/40 leading-relaxed">{profile?.location}</p>
          </div>

          {/* Links */}
          <div>
            <p className="text-xs font-mono tracking-widest uppercase text-snow/30 mb-4">Connect</p>
            <div className="flex flex-col gap-2">
              {profile?.linkedin_url && (
                <a href={profile.linkedin_url} target="_blank" rel="noopener noreferrer"
                  className="text-sm text-snow/60 hover:text-snow transition-colors">
                  LinkedIn
                </a>
              )}
              {profile?.credly_url && (
                <a href={profile.credly_url} target="_blank" rel="noopener noreferrer"
                  className="text-sm text-snow/60 hover:text-snow transition-colors">
                  Credly Badges
                </a>
              )}
              {profile?.email && (
                <a href={`mailto:${profile.email}`}
                  className="text-sm text-snow/60 hover:text-snow transition-colors">
                  {profile.email}
                </a>
              )}
            </div>
          </div>

          {/* Quick stats */}
          <div>
            <p className="text-xs font-mono tracking-widest uppercase text-snow/30 mb-4">At a Glance</p>
            <div className="flex flex-col gap-2">
              <p className="text-sm text-snow/60">{profile?.years_experience}+ Years Experience</p>
              <p className="text-sm text-snow/60">{profile?.solutions_delivered}+ Enterprise AI Solutions</p>
              {profile?.visa_info && <p className="text-sm text-snow/60">{profile.visa_info}</p>}
            </div>
          </div>
        </div>

        <div className="border-t border-ink-muted pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-xs text-snow/30 font-mono">
            Built with FastAPI + React + PostgreSQL
          </p>
          <p className="text-xs text-snow/20">
            &copy; {new Date().getFullYear()} Praveen T N. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}

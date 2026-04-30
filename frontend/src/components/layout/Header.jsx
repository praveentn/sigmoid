import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const NAV = [
  { label: 'About', href: '#about' },
  { label: 'Experience', href: '#experience' },
  { label: 'Work', href: '#projects' },
  { label: 'Education', href: '#education' },
  { label: 'Research', href: '#research' },
]

export default function Header({ profile }) {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 40)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-snow/95 backdrop-blur-sm border-b border-cloud shadow-sm' : 'bg-transparent'
      }`}
    >
      <div className="max-w-6xl mx-auto px-6 md:px-12 flex items-center justify-between h-16">
        {/* Logo */}
        <a href="#" className="flex flex-col leading-none">
          <span className={`font-bold text-sm tracking-wide transition-colors ${scrolled ? 'text-ink' : 'text-snow'}`}>
            {profile?.name || 'Praveen T N'}
          </span>
          <span className={`text-xs font-mono transition-colors ${scrolled ? 'text-silver' : 'text-snow/60'}`}>
            AI & Data Architect
          </span>
        </a>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-8">
          {NAV.map(({ label, href }) => (
            <a
              key={label}
              href={href}
              className={`text-xs font-medium tracking-widest uppercase transition-colors hover:opacity-100 ${
                scrolled ? 'text-graphite hover:text-ink' : 'text-snow/70 hover:text-snow'
              }`}
            >
              {label}
            </a>
          ))}
          <a
            href={`mailto:${profile?.email || 'sigmoidptn@gmail.com'}`}
            className={`text-xs font-medium tracking-widest uppercase px-4 py-2 border transition-colors ${
              scrolled
                ? 'border-ink text-ink hover:bg-ink hover:text-snow'
                : 'border-snow/60 text-snow hover:bg-snow hover:text-ink'
            }`}
          >
            Contact
          </a>
        </nav>

        {/* Mobile menu button */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className={`md:hidden p-2 ${scrolled ? 'text-ink' : 'text-snow'}`}
        >
          <div className="w-5 h-4 flex flex-col justify-between">
            <span className={`block h-px bg-current transition-all ${menuOpen ? 'rotate-45 translate-y-[7px]' : ''}`} />
            <span className={`block h-px bg-current transition-all ${menuOpen ? 'opacity-0' : ''}`} />
            <span className={`block h-px bg-current transition-all ${menuOpen ? '-rotate-45 -translate-y-[9px]' : ''}`} />
          </div>
        </button>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden bg-ink border-t border-ink-muted">
          {NAV.map(({ label, href }) => (
            <a
              key={label}
              href={href}
              onClick={() => setMenuOpen(false)}
              className="block px-6 py-3 text-sm text-snow/80 hover:text-snow border-b border-ink-muted"
            >
              {label}
            </a>
          ))}
          <a
            href={`mailto:${profile?.email}`}
            className="block px-6 py-3 text-sm text-snow/80 hover:text-snow"
          >
            Contact
          </a>
        </div>
      )}
    </header>
  )
}

import { useEffect, useRef, useState } from 'react'

function Counter({ value }) {
  const [display, setDisplay] = useState('0')
  const ref = useRef(null)
  const animated = useRef(false)

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !animated.current) {
        animated.current = true
        // Extract numeric part
        const numMatch = value.match(/(\d+)/)
        if (!numMatch) { setDisplay(value); return }
        const num = parseInt(numMatch[1])
        const suffix = value.replace(/\d+/, '')
        let start = 0
        const duration = 1800
        const step = (timestamp) => {
          if (!start) start = timestamp
          const progress = Math.min((timestamp - start) / duration, 1)
          const eased = 1 - Math.pow(1 - progress, 3)
          setDisplay(Math.floor(eased * num) + suffix)
          if (progress < 1) requestAnimationFrame(step)
        }
        requestAnimationFrame(step)
      }
    }, { threshold: 0.3 })
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [value])

  return <span ref={ref}>{display}</span>
}

export default function Impact({ metrics }) {
  if (!metrics?.length) return null

  return (
    <section className="bg-ink py-20 -mt-1">
      <div className="section-container">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-px bg-ink-muted border border-ink-muted">
          {metrics.map((m, i) => (
            <div
              key={m.id}
              className="bg-ink-soft p-8 flex flex-col gap-1 hover:bg-ink-mid transition-colors group"
            >
              <span className="text-3xl md:text-4xl font-black text-snow tracking-tight">
                <Counter value={m.metric} />
              </span>
              <span className="text-xs font-semibold text-snow/70 tracking-wide leading-tight mt-1">
                {m.label}
              </span>
              <span className="text-xs text-snow/30 leading-snug mt-1 hidden group-hover:block">
                {m.description}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

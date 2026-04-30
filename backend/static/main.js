// ── Header scroll effect ─────────────────────────────────────
const header = document.querySelector('.site-header');
if (header) {
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 40);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// ── Scroll reveal ────────────────────────────────────────────
const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObserver.unobserve(e.target); } });
}, { threshold: 0.07 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Counter animation ─────────────────────────────────────────
function animateCounter(el) {
  const raw = el.dataset.target;
  const numMatch = raw.match(/(\d+)/);
  if (!numMatch) { el.textContent = raw; return; }
  const num = parseInt(numMatch[1]);
  const suffix = raw.replace(/\d+/, '');
  let start = null;
  const duration = 1800;
  const step = (ts) => {
    if (!start) start = ts;
    const progress = Math.min((ts - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * num) + suffix;
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

const counterObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      animateCounter(e.target);
      counterObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.4 });
document.querySelectorAll('.impact-metric[data-target]').forEach(el => counterObserver.observe(el));

// ── Experience accordion ──────────────────────────────────────
document.querySelectorAll('.exp-card').forEach(card => {
  card.addEventListener('click', () => {
    const item = card.closest('.exp-item');
    const wasOpen = item.classList.contains('open');
    document.querySelectorAll('.exp-item').forEach(i => i.classList.remove('open'));
    if (!wasOpen) item.classList.add('open');
  });
});
// Open first experience by default
const firstExp = document.querySelector('.exp-item');
if (firstExp) firstExp.classList.add('open');

// ── Project category filter ───────────────────────────────────
const filterBtns = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.dataset.cat;
    projectCards.forEach(card => {
      const match = cat === 'all' || card.dataset.category === cat;
      card.style.display = match ? '' : 'none';
    });
  });
});

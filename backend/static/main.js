// ── Mobile nav ────────────────────────────────────────────────
const navToggle = document.getElementById('navToggle');
const mobileNav = document.getElementById('mobileNav');

function openMobileNav() {
  navToggle?.classList.add('open');
  mobileNav?.classList.add('open');
  navToggle?.setAttribute('aria-expanded', 'true');
  mobileNav?.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}
function closeMobileNav() {
  navToggle?.classList.remove('open');
  mobileNav?.classList.remove('open');
  navToggle?.setAttribute('aria-expanded', 'false');
  mobileNav?.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}
navToggle?.addEventListener('click', () => {
  navToggle.classList.contains('open') ? closeMobileNav() : openMobileNav();
});
mobileNav?.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMobileNav));
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMobileNav(); });

// ── Nav scrollspy ─────────────────────────────────────────────
const NAV_SECTIONS = ['about','experience','projects','education','research','contact'];
const navLinkMap = {};
NAV_SECTIONS.forEach(id => {
  const desktop = document.querySelector(`.header-nav a[href="#${id}"]`);
  const mobile  = document.querySelector(`.mobile-nav a[href="#${id}"]`);
  navLinkMap[id] = [desktop, mobile].filter(Boolean);
});
const spyObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      Object.values(navLinkMap).flat().forEach(l => l.classList.remove('active'));
      (navLinkMap[e.target.id] || []).forEach(l => l.classList.add('active'));
    }
  });
}, { threshold: 0.15, rootMargin: '-10% 0px -65% 0px' });
NAV_SECTIONS.forEach(id => {
  const el = document.getElementById(id);
  if (el) spyObserver.observe(el);
});

// ── Header scroll effect ──────────────────────────────────────
const header = document.querySelector('.site-header');
if (header) {
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 40);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// ── Scroll reveal ─────────────────────────────────────────────
const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObserver.unobserve(e.target); } });
}, { threshold: 0.07 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Dynamic years of experience (live, decimal) ───────────────
const YOE_START = new Date(2010, 2, 1); // March 1, 2010
function calcYoE(decimals = 1) {
  return ((Date.now() - YOE_START) / (365.25 * 24 * 3600 * 1000)).toFixed(decimals);
}
function updateYoE() {
  const val = calcYoE();
  document.querySelectorAll('[data-yoe-live]').forEach(el => { el.textContent = val; });
  document.querySelectorAll('[data-yoe-live-inline]').forEach(el => { el.textContent = val; });
}
updateYoE();
setInterval(updateYoE, 30000); // refresh every 30s

// ── Counter animation ─────────────────────────────────────────
function animateCounter(el) {
  if (el.hasAttribute('data-yoe-live')) return; // handled by live counter
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
    if (e.isIntersecting) { animateCounter(e.target); counterObserver.unobserve(e.target); }
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
const firstExp = document.querySelector('.exp-item');
if (firstExp) firstExp.classList.add('open');

// ── Projects: category + company filter ──────────────────────
let activeGroup = 'category';

const groupBtns = document.querySelectorAll('.group-btn');
const filterCat = document.getElementById('filter-category');
const filterCo = document.getElementById('filter-company');
const projectCards = document.querySelectorAll('.project-card');

groupBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    groupBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeGroup = btn.dataset.group;
    if (activeGroup === 'category') {
      filterCat.style.display = '';
      filterCo.style.display = 'none';
      filterCat.querySelector('.filter-btn[data-cat="all"]')?.click();
    } else {
      filterCat.style.display = 'none';
      filterCo.style.display = '';
      filterCo.querySelector('.filter-btn[data-company="all"]')?.click();
    }
  });
});

document.querySelectorAll('#filter-category .filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('#filter-category .filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.dataset.cat;
    projectCards.forEach(card => {
      card.style.display = (cat === 'all' || card.dataset.category === cat) ? '' : 'none';
    });
  });
});

document.querySelectorAll('#filter-company .filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('#filter-company .filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const co = btn.dataset.company;
    projectCards.forEach(card => {
      const match = co === 'all' || card.dataset.company === co ||
                    (card.dataset.company && card.dataset.company.startsWith(co));
      card.style.display = match ? '' : 'none';
    });
  });
});

// ── Search overlay ────────────────────────────────────────────
const searchOverlay = document.getElementById('searchOverlay');
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
const searchTrigger = document.getElementById('searchTrigger');
const SEARCH_INDEX = window.SEARCH_INDEX || {};
let searchHighlightIdx = -1;

function openSearch() {
  searchOverlay?.classList.add('open');
  searchInput?.focus();
  document.body.style.overflow = 'hidden';
}
function closeSearch() {
  searchOverlay?.classList.remove('open');
  if (searchInput) searchInput.value = '';
  if (searchResults) searchResults.innerHTML = '';
  document.body.style.overflow = '';
  searchHighlightIdx = -1;
}

searchTrigger?.addEventListener('click', openSearch);
searchOverlay?.addEventListener('click', e => { if (e.target === searchOverlay) closeSearch(); });

document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); openSearch(); }
  if (e.key === 'Escape' && searchOverlay?.classList.contains('open')) closeSearch();
  if (!searchOverlay?.classList.contains('open')) return;
  const items = searchResults?.querySelectorAll('.search-result-item');
  if (!items?.length) return;
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    searchHighlightIdx = Math.min(searchHighlightIdx + 1, items.length - 1);
    items.forEach((el, i) => el.classList.toggle('highlighted', i === searchHighlightIdx));
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    searchHighlightIdx = Math.max(searchHighlightIdx - 1, 0);
    items.forEach((el, i) => el.classList.toggle('highlighted', i === searchHighlightIdx));
  } else if (e.key === 'Enter' && searchHighlightIdx >= 0) {
    items[searchHighlightIdx]?.click();
  }
});

function tokenScore(query, text) {
  if (!text) return 0;
  const q = query.toLowerCase();
  const t = text.toLowerCase();
  if (t.includes(q)) return 2;
  const tokens = q.split(/\s+/);
  return tokens.filter(tok => t.includes(tok)).length / tokens.length;
}

function runSearch(query) {
  searchHighlightIdx = -1;
  if (!query.trim()) { searchResults.innerHTML = ''; return; }
  const q = query.toLowerCase().trim();
  const hits = [];

  (SEARCH_INDEX.projects || []).forEach(p => {
    const score = Math.max(
      tokenScore(q, p.name) * 3,
      tokenScore(q, p.description),
      tokenScore(q, p.company),
      tokenScore(q, p.category),
      ...(p.tech || []).map(t => tokenScore(q, t))
    );
    if (score > 0) hits.push({ type: 'Project', name: p.name, sub: p.company + ' · ' + p.category, section: '#projects', score });
  });
  (SEARCH_INDEX.experience || []).forEach(e => {
    const score = Math.max(
      tokenScore(q, e.company) * 3,
      tokenScore(q, e.role) * 2,
      ...(e.highlights || []).map(h => tokenScore(q, h))
    );
    if (score > 0) hits.push({ type: 'Experience', name: e.role, sub: e.company, section: '#experience', score });
  });
  (SEARCH_INDEX.skills || []).forEach(s => {
    const score = Math.max(
      tokenScore(q, s.category) * 2,
      ...(s.items || []).map(i => tokenScore(q, i) * 1.5)
    );
    if (score > 0) hits.push({ type: 'Skill', name: s.category, sub: (s.items || []).slice(0, 4).join(', '), section: '#skills', score });
  });
  (SEARCH_INDEX.research || []).forEach(r => {
    const score = Math.max(tokenScore(q, r.title) * 3, tokenScore(q, r.description), tokenScore(q, r.focus_area));
    if (score > 0) hits.push({ type: 'Research', name: r.title, sub: r.focus_area, section: '#research', score });
  });

  hits.sort((a, b) => b.score - a.score);
  const top = hits.slice(0, 8);

  if (!top.length) {
    searchResults.innerHTML = '<div class="search-empty">No results found.</div>';
    return;
  }

  const byType = {};
  top.forEach(h => { (byType[h.type] = byType[h.type] || []).push(h); });

  let html = '';
  Object.entries(byType).forEach(([type, items]) => {
    html += `<div class="search-result-section">${type}</div>`;
    items.forEach(item => {
      html += `<div class="search-result-item" data-section="${item.section}">
        <span class="search-result-type">${type}</span>
        <div><div class="search-result-name">${item.name}</div><div class="search-result-sub">${item.sub || ''}</div></div>
      </div>`;
    });
  });
  searchResults.innerHTML = html;

  searchResults.querySelectorAll('.search-result-item').forEach(el => {
    el.addEventListener('click', () => {
      const sec = el.dataset.section;
      closeSearch();
      if (sec) { setTimeout(() => { document.querySelector(sec)?.scrollIntoView({ behavior: 'smooth' }); }, 100); }
    });
  });
}

searchInput?.addEventListener('input', e => runSearch(e.target.value));

// ── SIGMA chat ────────────────────────────────────────────────
const sigmaTrigger = document.getElementById('sigmaTrigger');
const sigmaOverlay = document.getElementById('sigmaOverlay');
const sigmaClose   = document.getElementById('sigmaClose');
const sigmaMessages = document.getElementById('sigmaMessages');
const sigmaInput   = document.getElementById('sigmaInput');
const sigmaSend    = document.getElementById('sigmaSend');
const sigmaStop    = document.getElementById('sigmaStop');
const sigmaLimit   = document.getElementById('sigmaLimit');

let sigmaSessionId = sessionStorage.getItem('sigma_session') || (() => {
  const id = 'sess_' + Math.random().toString(36).slice(2);
  sessionStorage.setItem('sigma_session', id);
  return id;
})();

let sigmaHistory   = [];
let sigmaRemaining = 20;
let sigmaActive    = false;       // true while fetching or typing
let sigmaAbort     = null;        // AbortController
let sigmaStopType  = false;       // signal to stop typewriter mid-run

function openSigma() {
  sigmaOverlay?.classList.add('open');
  document.body.style.overflow = 'hidden';
  sigmaInput?.focus();
}
function closeSigma() {
  sigmaOverlay?.classList.remove('open');
  document.body.style.overflow = '';
}

sigmaTrigger?.addEventListener('click', openSigma);
sigmaClose?.addEventListener('click', closeSigma);
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && sigmaOverlay?.classList.contains('open')) closeSigma();
});

// Suggested questions
document.querySelectorAll('.sigma-suggest').forEach(btn => {
  btn.addEventListener('click', () => {
    if (sigmaInput) sigmaInput.value = btn.dataset.q;
    sendSigmaMessage();
  });
});

// Auto-resize textarea
sigmaInput?.addEventListener('input', () => {
  sigmaInput.style.height = 'auto';
  sigmaInput.style.height = Math.min(sigmaInput.scrollHeight, 120) + 'px';
});
sigmaInput?.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendSigmaMessage(); }
});
sigmaSend?.addEventListener('click', sendSigmaMessage);

// Stop button — abort fetch or halt typewriter
sigmaStop?.addEventListener('click', () => {
  sigmaStopType = true;
  sigmaAbort?.abort();
  setGenerating(false);
});

function setGenerating(on) {
  sigmaActive = on;
  if (sigmaSend) sigmaSend.style.display = on ? 'none' : 'flex';
  if (sigmaStop) sigmaStop.style.display = on ? 'flex' : 'none';
  if (sigmaInput) sigmaInput.disabled = on;
}

function addMessage(role) {
  if (!sigmaMessages) return null;
  const div = document.createElement('div');
  div.className = `sigma-msg sigma-msg--${role === 'user' ? 'user' : 'agent'}`;
  const badge = document.createElement('div');
  badge.className = 'sigma-msg-badge';
  badge.textContent = role === 'user' ? 'YOU' : 'SIGMA';
  const textDiv = document.createElement('div');
  textDiv.className = 'sigma-msg-text';
  div.appendChild(badge);
  div.appendChild(textDiv);
  sigmaMessages.appendChild(div);
  sigmaMessages.scrollTop = sigmaMessages.scrollHeight;
  return textDiv;
}

function typeText(el, text, speed = 16) {
  sigmaStopType = false;
  return new Promise(resolve => {
    const chars = [...text];
    let i = 0;
    const tick = setInterval(() => {
      if (sigmaStopType) {
        clearInterval(tick);
        resolve();
        return;
      }
      el.textContent += chars[i++] || '';
      sigmaMessages.scrollTop = sigmaMessages.scrollHeight;
      if (i >= chars.length) { clearInterval(tick); resolve(); }
    }, speed);
  });
}

function showTyping() {
  const div = document.createElement('div');
  div.className = 'sigma-msg sigma-msg--agent';
  div.id = 'sigma-typing-ind';
  const badge = document.createElement('div');
  badge.className = 'sigma-msg-badge';
  badge.textContent = 'SIGMA';
  const dots = document.createElement('div');
  dots.className = 'sigma-typing';
  dots.innerHTML = '<span></span><span></span><span></span>';
  div.appendChild(badge);
  div.appendChild(dots);
  sigmaMessages?.appendChild(div);
  sigmaMessages.scrollTop = sigmaMessages.scrollHeight;
}
function hideTyping() {
  document.getElementById('sigma-typing-ind')?.remove();
}

async function sendSigmaMessage() {
  const text = sigmaInput?.value.trim();
  if (!text || sigmaActive) return;

  sigmaInput.value = '';
  sigmaInput.style.height = 'auto';

  const userEl = addMessage('user');
  if (userEl) userEl.textContent = text;
  sigmaHistory.push({ role: 'user', content: text });

  if (sigmaRemaining <= 0) {
    const el = addMessage('agent');
    if (el) await typeText(el, "You've reached today's query limit. Please come back later.");
    return;
  }

  setGenerating(true);
  showTyping();
  sigmaAbort = new AbortController();

  let reply = '';
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      signal: sigmaAbort.signal,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: sigmaHistory, session_id: sigmaSessionId }),
    });
    const data = await res.json();

    if (data.remaining !== undefined) {
      sigmaRemaining = data.remaining;
      if (sigmaLimit) sigmaLimit.textContent =
        `${sigmaRemaining} quer${sigmaRemaining === 1 ? 'y' : 'ies'} remaining`;
    }
    reply = data.reply || data.error || 'Something went wrong. Please try again.';
  } catch (err) {
    if (err.name === 'AbortError') {
      reply = ''; // user stopped — don't show anything
    } else {
      reply = 'Connection error. Please try again.';
    }
  }

  hideTyping();
  setGenerating(false);

  if (reply) {
    const agentEl = addMessage('agent');
    if (agentEl) await typeText(agentEl, reply);
    sigmaHistory.push({ role: 'model', content: reply });
    if (sigmaHistory.length > 20) sigmaHistory = sigmaHistory.slice(-20);
  }

  sigmaInput?.focus();
}

(() => {
  'use strict';
  const registry = Array.isArray(window.UTILITY_TOOLS) ? window.UTILITY_TOOLS : [];
  const grid = document.getElementById('tool-grid');
  const search = document.getElementById('search-tools');
  const filters = document.getElementById('filters');
  const status = document.getElementById('results-status');
  const noResults = document.getElementById('no-results');
  const reset = document.getElementById('reset-search');
  const menuButton = document.getElementById('menu-toggle');
  const nav = document.getElementById('main-nav');
  let activeCategory = 'all';

  const el = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = String(text);
    return node;
  };

  const allowedUrl = (raw) => {
    try {
      const url = new URL(raw);
      return url.protocol === 'https:' ? url.href : null;
    } catch { return null; }
  };

  function link(label, url, className) {
    const anchor = el('a', className, label);
    const safe = allowedUrl(url);
    if (safe) {
      anchor.href = safe;
      anchor.target = '_blank';
      anchor.rel = 'noopener noreferrer';
    } else {
      anchor.removeAttribute('href');
      anchor.setAttribute('aria-disabled', 'true');
    }
    return anchor;
  }

  function makeCard(tool, index) {
    const card = el('article', 'tool-card');
    card.dataset.toolId = tool.id;
    const imgContainer = el('div', 'tool-image-wrap');
    const img = el('img', 'tool-image');
    img.src = tool.image;
    img.alt = tool.imageAlt || '';
    img.width = 880;
    img.height = 500;
    img.loading = index === 0 ? 'eager' : 'lazy';
    imgContainer.append(img);
    imgContainer.append(el('span', 'image-corner', 'UTILITY / ' + String(index + 1).padStart(3, '0')));
    const imageBottom = el('div', 'image-bottom');
    imageBottom.append(el('span', 'image-index', 'DIGITAL WORKSPACE'));
    imageBottom.append(el('span', 'image-badge', '● ONLINE'));
    imgContainer.append(imageBottom);
    const info = el('div', 'tool-info');
    const caption = el('div', 'tool-caption');
    caption.append(el('span', 'tool-caption-id', 'MODULE / ' + String(index + 1).padStart(3, '0')));
    caption.append(el('span', 'tool-caption-status', 'LIVE SERVICE'));
    info.append(caption);
    info.append(el('h3', 'tool-name', tool.name));
    info.append(el('p', 'tool-subtitle', tool.subtitle));
    info.append(el('p', 'tool-description', tool.description));
    const tags = el('div', 'tool-tags');
    (tool.tags || []).slice(0, 4).forEach((tag) => tags.append(el('span', 'tool-tag', tag)));
    info.append(tags);
    const actions = el('div', 'tool-actions');
    actions.append(link('서비스 실행 ↗', tool.url, 'tool-primary-link'));
    if (tool.repository) actions.append(link('GitHub 소스 ↗', tool.repository, 'tool-secondary-link'));
    info.append(actions);
    card.append(imgContainer, info);
    return card;
  }

  function normalize(value) {
    return String(value || '').toLocaleLowerCase('ko').normalize('NFKC').trim();
  }

  function render() {
    const query = normalize(search.value);
    const visible = registry.filter((tool) => {
      if (tool.status !== 'live' || !allowedUrl(tool.url)) return false;
      if (activeCategory !== 'all' && !(tool.category || []).includes(activeCategory)) return false;
      return !query || normalize([tool.name, tool.subtitle, tool.description, ...(tool.tags || [])].join(' ')).includes(query);
    });
    const fragment = document.createDocumentFragment();
    visible.forEach((tool, i) => fragment.append(makeCard(tool, i)));
    grid.replaceChildren(fragment);
    noResults.hidden = visible.length > 0;
    status.replaceChildren(document.createTextNode('현재 이용 가능한 도구 '));
    status.append(el('strong', '', visible.length + '개'));
  }

  const liveCount = registry.filter((t) => t.status === 'live' && allowedUrl(t.url)).length;
  document.getElementById('hero-live-count').textContent = String(liveCount).padStart(2, '0');
  document.getElementById('module-index').textContent = String(liveCount).padStart(2, '0') + ' ACTIVE';
  document.getElementById('year').textContent = new Date().getFullYear();
  search.addEventListener('input', render);
  filters.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-category]');
    if (!button || !filters.contains(button)) return;
    activeCategory = button.dataset.category;
    filters.querySelectorAll('button').forEach((b) => {
      const selected = b === button;
      b.classList.toggle('active', selected);
      b.setAttribute('aria-pressed', String(selected));
    });
    render();
  });
  reset.addEventListener('click', () => {
    search.value = '';
    const all = filters.querySelector('[data-category="all"]');
    if (all) all.click();
    search.focus();
  });
  document.addEventListener('keydown', (event) => {
    const target = event.target;
    const editing = target instanceof HTMLElement && (['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName) || target.isContentEditable);
    if (event.key === '/' && !editing && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault(); search.focus();
    }
  });
  menuButton.addEventListener('click', () => {
    const opened = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!opened));
    menuButton.setAttribute('aria-label', opened ? '메뉴 열기' : '메뉴 닫기');
    nav.classList.toggle('open', !opened);
  });
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) {
      nav.classList.remove('open');
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.setAttribute('aria-label', '메뉴 열기');
    }
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && nav.classList.contains('open')) {
      nav.classList.remove('open');
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.setAttribute('aria-label', '메뉴 열기');
      menuButton.focus();
    }
  });
  render();
})();

(() => {
  const steps = [
    { state: '|00⟩', values: [100, 0, 0, 0], text: '初态 |00⟩：测量必得 00。' },
    { state: '(|00⟩ + |10⟩) / √2', values: [50, 0, 50, 0], text: 'H 作用于 q₀：理想测量时，00 与 10 各约占一半。' },
    { state: '(|00⟩ + |11⟩) / √2', values: [50, 0, 0, 50], text: 'CX 将 q₀ 与 q₁ 关联：理想测量只出现 00 或 11。' },
    { state: '00 或 11', values: [50, 0, 0, 50], text: '一次测量只得到 00 或 11 中的一个；重复运行才看到接近 50/50 的分布。' }
  ];
  const stepButtons = [...document.querySelectorAll('.step-btn')];
  const barIds = ['00', '01', '10', '11'];
  function showStep(index) {
    const step = steps[index];
    stepButtons.forEach((button, i) => {
      button.classList.toggle('is-active', i === index);
      button.setAttribute('aria-pressed', String(i === index));
    });
    document.querySelectorAll('[data-gate]').forEach(gate => {
      gate.classList.toggle('is-on', Number(gate.dataset.gate) <= index);
    });
    document.getElementById('state-label').textContent = step.state;
    document.getElementById('sim-explain').textContent = step.text;
    barIds.forEach((id, i) => {
      document.getElementById(`bar-${id}`).style.width = `${step.values[i]}%`;
      document.getElementById(`val-${id}`).textContent = `${step.values[i]}%`;
    });
  }
  stepButtons.forEach(button => button.addEventListener('click', () => showStep(Number(button.dataset.step))));
  showStep(0);

  const trackButtons = [...document.querySelectorAll('.track')];
  const stages = [...document.querySelectorAll('.stage')];
  trackButtons.forEach(button => button.addEventListener('click', () => {
    const selected = button.dataset.track;
    trackButtons.forEach(item => {
      item.classList.toggle('active', item === button);
      item.setAttribute('aria-pressed', String(item === button));
    });
    stages.forEach(stage => { stage.hidden = selected !== 'all' && !stage.dataset.track.split(' ').includes(selected); });
  }));
  trackButtons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === 0)));

  const resourceButtons = [...document.querySelectorAll('.resource-filter')];
  const resources = [...document.querySelectorAll('.resource')];
  resourceButtons.forEach(button => button.addEventListener('click', () => {
    const selected = button.dataset.filter;
    resourceButtons.forEach(item => {
      item.classList.toggle('active', item === button);
      item.setAttribute('aria-pressed', String(item === button));
    });
    resources.forEach(resource => { resource.hidden = selected !== 'all' && resource.dataset.category !== selected; });
  }));
  resourceButtons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === 0)));

  const progressInputs = [...document.querySelectorAll('[data-progress]')];
  const storageKey = 'quantum-pqc-atlas-progress-v1';
  let saved = [];
  try { saved = JSON.parse(localStorage.getItem(storageKey) || '[]'); } catch (_) { saved = []; }
  if (!Array.isArray(saved)) saved = [];
  progressInputs.forEach(input => { input.checked = saved.includes(input.dataset.progress); });
  function updateProgress() {
    const completed = progressInputs.filter(input => input.checked).map(input => input.dataset.progress);
    document.getElementById('progress-text').textContent = `${completed.length} / ${progressInputs.length} 已完成`;
    document.getElementById('progress-bar').style.width = `${completed.length / progressInputs.length * 100}%`;
    try { localStorage.setItem(storageKey, JSON.stringify(completed)); } catch (_) { /* Browsing without persistent storage still works. */ }
  }
  progressInputs.forEach(input => input.addEventListener('change', updateProgress));
  document.getElementById('reset-progress').addEventListener('click', () => {
    progressInputs.forEach(input => { input.checked = false; });
    updateProgress();
  });
  updateProgress();

  const navLinks = [...document.querySelectorAll('.side-nav a[href^="#"]')];
  const sections = navLinks.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (!visible.length) return;
      navLinks.forEach(link => link.classList.toggle('active', link.getAttribute('href') === `#${visible[0].target.id}`));
    }, { rootMargin: '-70px 0px -65% 0px', threshold: 0 });
    sections.forEach(section => observer.observe(section));
  }
})();

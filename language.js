(()=>{
  const key='shundazhang-atlas-language';
  const isChinese=/\.zh\.html$/.test(location.pathname);
  let preferred=null;
  try { preferred=localStorage.getItem(key); } catch (_) {}
  if(preferred && preferred!==(isChinese?'zh':'en')) {
    const path=isChinese?location.pathname.replace(/\.zh\.html$/,'.html'):
      location.pathname.endsWith('/')?location.pathname+'index.zh.html':
      location.pathname.replace(/\.html$/,'.zh.html');
    if(path!==location.pathname) { location.replace(path+location.search+location.hash); return; }
  }
  document.addEventListener('click',event=>{
    const link=event.target.closest?.('[data-atlas-lang]');
    if(link)try { localStorage.setItem(key,link.dataset.atlasLang); } catch (_) {}
  },true);
})();

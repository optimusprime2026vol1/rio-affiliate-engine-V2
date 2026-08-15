(function(){
  'use strict';
  const STORAGE_KEY='rio_events';
  function safeRead(){
    try { const v=JSON.parse(localStorage.getItem(STORAGE_KEY)||'[]'); return Array.isArray(v)?v:[]; }
    catch (_) { return []; }
  }
  function trackOutboundClick(offerId,placement,status){
    const event={event:'affiliate_click_intent',offer_id:offerId||'unknown',placement:placement||'unknown',link_status:status||'unknown',timestamp:new Date().toISOString(),path:location.pathname};
    const prior=safeRead(); prior.push(event); if(prior.length>200) prior.splice(0,prior.length-200);
    try { localStorage.setItem(STORAGE_KEY,JSON.stringify(prior)); } catch (_) {}
    if(window.RIO_DEBUG) console.log('RIO event',event);
  }
  document.querySelectorAll('[data-offer]').forEach(function(el){
    el.addEventListener('click',function(e){
      const disabled=el.getAttribute('aria-disabled')==='true';
      if(disabled) e.preventDefault();
      trackOutboundClick(el.dataset.offer,el.dataset.placement,disabled?'pending':'active');
    });
  });
})();

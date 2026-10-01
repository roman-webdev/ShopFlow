'use strict';
/* Progressive motion: no scroll interception, animation loop, or external dependency. */
(() => {
 const reduced=matchMedia('(prefers-reduced-motion: reduce)'), fine=matchMedia('(hover: hover) and (pointer: fine)');
 const allowed=()=>!reduced.matches&&fine.matches;
 const closing=new WeakSet();
 function close(dialog){if(!dialog?.open||closing.has(dialog))return Promise.resolve();if(reduced.matches){dialog.close();return Promise.resolve();}closing.add(dialog);dialog.classList.add('is-closing');return new Promise(resolve=>setTimeout(()=>{dialog.close();dialog.classList.remove('is-closing');closing.delete(dialog);resolve();},260));}
 function bump(el){if(!el||reduced.matches)return;el.classList.remove('bag-bump');requestAnimationFrame(()=>el.classList.add('bag-bump'));}
 window.ShopFlowMotion={close,bump};
 document.querySelectorAll('dialog').forEach(dialog=>dialog.addEventListener('cancel',e=>{e.preventDefault();close(dialog);}));
 let card=null,button=null,frame=0,lastPointer=null;
 function clearCard(){card?.style.removeProperty('--tilt-x');card?.style.removeProperty('--tilt-y');card=null;}
 function clearButton(){if(button)button.style.transform='';button=null;}
 function pointer(){frame=0;if(!allowed()||!lastPointer)return;const e=lastPointer;
 const target=e.target.closest?.('.product-photo');if(card!==target){clearCard();card=target;}
 if(card){const r=card.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;card.style.setProperty('--tilt-x',`${(y-.5)*-9}deg`);card.style.setProperty('--tilt-y',`${(x-.5)*10}deg`);card.style.setProperty('--light-x',`${x*100}%`);card.style.setProperty('--light-y',`${y*100}%`);}
 const next=e.target.closest?.('.hero .primary,.newsletter .primary');if(button!==next){clearButton();button=next;}
 if(button){const r=button.getBoundingClientRect();button.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.08}px,${(e.clientY-r.top-r.height/2)*.12}px)`;}
 const scene=e.target.closest?.('.hero-image');if(scene){const r=scene.getBoundingClientRect();scene.style.setProperty('--scene-x',`${((e.clientX-r.left)/r.width-.5)*30}px`);scene.style.setProperty('--scene-y',`${((e.clientY-r.top)/r.height-.5)*25}px`);}else{document.querySelector('.hero-image')?.style.setProperty('--scene-x','0px');document.querySelector('.hero-image')?.style.setProperty('--scene-y','0px');}
 }
 document.addEventListener('pointermove',e=>{lastPointer=e;if(!frame)frame=requestAnimationFrame(pointer);},{passive:true});
 document.documentElement.addEventListener('pointerleave',()=>{clearCard();clearButton();});
 const hero=document.querySelector('.hero-image'),editorial=document.querySelector('.editorial-art');let scrollFrame=0;
 function scroll(){scrollFrame=0;const extent=document.documentElement.scrollHeight-innerHeight;document.querySelector('.header')?.style.setProperty('--progress',`${extent?scrollY/extent*100:0}%`);if(!allowed())return;if(hero){const r=hero.getBoundingClientRect();if(r.bottom>0&&r.top<innerHeight)hero.style.setProperty('--scroll-y',`${Math.max(-25,Math.min(25,-r.top*.07))}px`);}if(editorial){const r=editorial.getBoundingClientRect();if(r.bottom>0&&r.top<innerHeight)editorial.style.setProperty('--editorial-y',`${Math.max(-24,Math.min(24,(innerHeight/2-r.top)*.07))}px`);}}
 addEventListener('scroll',()=>{if(!scrollFrame)scrollFrame=requestAnimationFrame(scroll);},{passive:true});scroll();
 function reset(){clearCard();clearButton();hero?.style.removeProperty('--scene-x');hero?.style.removeProperty('--scene-y');hero?.style.removeProperty('--scroll-y');editorial?.style.removeProperty('--editorial-y');}
 const counter=document.querySelector('.hero-index');
 if(counter&&!reduced.matches){const counters=new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)return;counters.disconnect();const nodes=Array.from(counter.querySelectorAll('strong')),values=nodes.map(el=>Number(el.textContent)),started=performance.now();function tick(now){const progress=reduced.matches?1:Math.min(1,(now-started)/850),eased=1-Math.pow(1-progress,3);nodes.forEach((el,i)=>el.textContent=String(Math.round(values[i]*eased)).padStart(2,'0'));if(progress<1)requestAnimationFrame(tick);}requestAnimationFrame(tick);},{threshold:.3});counters.observe(counter);}
 reduced.addEventListener('change',reset);fine.addEventListener('change',reset);
})();

// Pause ambient animation while the page is in the background.
const syncAmbientVisibility=()=>document.body.classList.toggle('ambient-paused',document.hidden);
document.addEventListener('visibilitychange',syncAmbientVisibility);syncAmbientVisibility();


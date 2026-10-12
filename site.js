// Able · Generation 2.0 — the showcase site's behaviour: reading progress, the chapter rail, drawers and the image viewer.
(() => {
	const chapters = [...document.querySelectorAll('section.chapter')];
	const nodes = new Map([...document.querySelectorAll('.rail-node')].map(n => [n.dataset.target, n]));
	const picker = document.querySelector('#chapter-picker');
	const bar = document.querySelector('.progress span');
	const fill = document.querySelector('.rail-fill');

	// Reading progress, and the rail's playhead.
	function onScroll() {
		const max = document.documentElement.scrollHeight - innerHeight;
		const done = max > 0 ? scrollY / max : 0;
		bar.style.width = (done * 100).toFixed(2) + '%';
		fill.style.height = (done * 100).toFixed(2) + '%';
	}
	addEventListener('scroll', onScroll, { passive: true });
	onScroll();

	// The chapter in view lights up its keyframe; those before it are done.
	let current = null;
	function setActive(id) {
		if (id === current) return;
		current = id;
		let before = true;
		for (const [key, node] of nodes) {
			node.classList.toggle('active', key === id);
			node.classList.toggle('done', before && key !== id);
			if (key === id) before = false;
		}
		if (picker) picker.value = id || '';
	}
	const watcher = new IntersectionObserver(entries => {
		const visible = entries.filter(e => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
		if (visible.length) setActive(visible[0].target.id);
	}, { rootMargin: '-35% 0px -55% 0px' });
	chapters.forEach(c => watcher.observe(c));

	picker?.addEventListener('change', e => { if (e.target.value) location.hash = e.target.value; });

	// Every drawer at once.
	const toggle = document.querySelector('#details-toggle');
	toggle?.addEventListener('click', () => {
		const drawers = [...document.querySelectorAll('main details')];
		const open = !drawers.every(d => d.open);
		drawers.forEach(d => d.open = open);
		toggle.textContent = open ? 'Close every drawer' : 'Open every drawer';
	});

	// A link into a closed drawer opens it.
	function revealHash() {
		const key = decodeURIComponent(location.hash.slice(1));
		if (!key) return;
		const target = document.getElementById(key) || document.getElementsByName(key)[0];
		if (!target) return;
		let opened = false;
		for (let p = target.parentElement; p; p = p.parentElement) {
			if (p.tagName === 'DETAILS' && !p.open) { p.open = true; opened = true; }
		}
		if (opened) requestAnimationFrame(() => target.scrollIntoView());
	}
	addEventListener('hashchange', revealHash);
	revealHash();

	// The viewer: click a screenshot to enlarge it; arrows step through the screenshots that are showing.
	const viewer = document.querySelector('#viewer');
	const big = viewer.querySelector('img');
	const caption = viewer.querySelector('figcaption');
	let index = 0;
	const shown = () => [...document.querySelectorAll('main .shot img')].filter(img => img.offsetParent !== null);
	function show(img) {
		const list = shown();
		index = Math.max(0, list.indexOf(img));
		big.src = img.src;
		big.alt = img.alt;
		const cap = img.closest('figure')?.querySelector('figcaption');
		caption.innerHTML = cap ? cap.innerHTML : img.alt;
		if (!viewer.open) viewer.showModal();
	}
	function step(by) {
		const list = shown();
		if (list.length) show(list[(index + by + list.length) % list.length]);
	}
	document.querySelectorAll('main .shot img').forEach(img => {
		img.tabIndex = 0;
		img.addEventListener('click', () => show(img));
		img.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); show(img); } });
	});
	viewer.querySelector('.close').addEventListener('click', () => viewer.close());
	viewer.querySelector('.prev').addEventListener('click', e => { e.stopPropagation(); step(-1); });
	viewer.querySelector('.next').addEventListener('click', e => { e.stopPropagation(); step(1); });
	big.addEventListener('click', () => viewer.close());
	viewer.addEventListener('click', e => { if (e.target === viewer || e.target.tagName === 'FIGURE') viewer.close(); });
	addEventListener('keydown', e => {
		if (!viewer.open) return;
		if (e.key === 'ArrowRight') step(1);
		if (e.key === 'ArrowLeft') step(-1);
	});
})();

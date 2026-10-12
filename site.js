// Able · Generation 2.0 — the field manual's behaviour: the running header, the specs, and the figure viewer.
(() => {
	const chapters = [...document.querySelectorAll('section.chapter')];
	const whereN = document.querySelector('.where-n');
	const whereT = document.querySelector('.where-t');

	// The bar names the chapter being read, as a printed manual's running header does.
	function setWhere(section) {
		if (!section) { whereN.textContent = '—'; whereT.textContent = 'Contents'; return; }
		whereN.textContent = '§' + section.querySelector('.margin .big').textContent;
		whereT.textContent = section.querySelector('h2').textContent;
	}
	const watcher = new IntersectionObserver(entries => {
		const visible = entries.filter(e => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
		if (visible.length) setWhere(visible[0].target);
	}, { rootMargin: '-30% 0px -60% 0px' });
	chapters.forEach(c => watcher.observe(c));
	addEventListener('scroll', () => { if (chapters.length && scrollY < chapters[0].offsetTop - innerHeight * .3) setWhere(null); }, { passive: true });

	// Every spec at once.
	const toggle = document.querySelector('#specs-toggle');
	toggle?.addEventListener('click', () => {
		const specs = [...document.querySelectorAll('main details')];
		const open = !specs.every(d => d.open);
		specs.forEach(d => d.open = open);
		toggle.textContent = open ? 'Close all specs' : 'Open all specs';
	});

	// A link into a closed spec opens it.
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

	// The viewer: a figure enlarged with its number and caption; arrow keys step through the figures that are showing.
	const viewer = document.querySelector('#viewer');
	const big = viewer.querySelector('img');
	const caption = viewer.querySelector('figcaption');
	let index = 0;
	const shown = () => [...document.querySelectorAll('main .plate img')].filter(img => img.offsetParent !== null);
	function show(img) {
		index = Math.max(0, shown().indexOf(img));
		big.src = img.src;
		big.alt = img.alt;
		const figure = img.closest('figure');
		const no = figure?.querySelector('.fig-no')?.outerHTML || '';
		const cap = figure?.querySelector('figcaption');
		caption.innerHTML = no + (cap ? cap.innerHTML : img.alt);
		if (!viewer.open) viewer.showModal();
	}
	function step(by) {
		const list = shown();
		if (list.length) show(list[(index + by + list.length) % list.length]);
	}
	document.querySelectorAll('main .plate img').forEach(img => {
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

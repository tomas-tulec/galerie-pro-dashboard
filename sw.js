// Service worker — cachuje pouze app shell, data z API se vždy tahají online
const CACHE_NAME = 'galerie-ttf-shell-v3';
const SHELL_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icon-32.png',
  '/icon-180.png',
  '/icon-192.png',
  '/icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      cache.addAll(SHELL_FILES.map((u) => new Request(u, { cache: 'reload' })))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Data z WP REST API vždy jen z online sítě, nikdy z cache
  if (url.pathname.includes('/wp-json/')) {
    return;
  }

  if (event.request.method !== 'GET' || url.origin !== self.location.origin) {
    return;
  }

  // HTML dokument (navigace) — nejdřív síť, cache jen jako offline záloha,
  // aby se nová verze aplikace vždy nasadila hned po online spuštění
  const isDocument = event.request.mode === 'navigate' ||
    url.pathname === '/' || url.pathname === '/index.html';

  if (isDocument) {
    event.respondWith(
      fetch(event.request).then((resp) => {
        const copy = resp.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
        return resp;
      }).catch(() =>
        caches.match(event.request).then((c) => c || caches.match('/index.html'))
      )
    );
    return;
  }

  // Ostatní statické soubory (ikony, manifest) — nejdřív cache
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request).then((resp) => {
        const copy = resp.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
        return resp;
      }).catch(() => cached);
    })
  );
});

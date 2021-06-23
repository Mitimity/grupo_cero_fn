var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
    '/',
    '/filtro_tec/',
    '/buscar_obra/',
    '/buscar_autor/',
    '/cerrar_sesion/',
    '/mi_perfil/',
    '/ingresar_obra_adm/',
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});
self.addEventListener('fetch', function(event) {
    event.respondWith(

      fetch(event.request)
      .then((result)=>{
        return caches.open(CACHE_NAME)
        .then(function(c) {
          c.put(event.request.url, result.clone())
          return result;
        })
        
      })
      .catch(function(e){
          return caches.match(event.request)
      })
    );
});


//////////////////////////////////////////////////////////
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js');


var firebaseConfig = {
    apiKey: "AIzaSyBo8UAFK58gww_RqPiQGTMWwTCoxSqmJ40",
    authDomain: "djangosec002-28183.firebaseapp.com",
    projectId: "djangosec002-28183",
    storageBucket: "djangosec002-28183.appspot.com",
    messagingSenderId: "61778552818",
    appId: "1:61778552818:web:7b7ae281aff9bacab5ad6b"
  };
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

////////////////////////////////////////////////////////////
let messaging = firebase.messaging();
/////////////// modelo de notificacion offline ////////////
messaging.setBackgroundMessageHandler(function(payload) {
  let titulo = payload.notification.title
  let opciones = {
      body: payload.notification.body,
      icon: payload.notification.icon
  }
  self.registration.showNotification(titulo, opciones)
})

////////////////////////////////////////////////////////////

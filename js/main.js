/* =============================================
   ZONA INFORMÁTICA PONTEVEDRA - Main JS
   ============================================= */

document.addEventListener('DOMContentLoaded', function () {

  // --- Cookie banner ---
  const banner = document.getElementById('cookieBanner');
  const acceptBtn = document.getElementById('cookieAccept');
  const rejectBtn = document.getElementById('cookieReject');

  if (banner) {
    if (!localStorage.getItem('cookieConsent')) {
      setTimeout(function () { banner.classList.add('is-visible'); }, 1200);
    }

    if (acceptBtn) {
      acceptBtn.addEventListener('click', function () {
        localStorage.setItem('cookieConsent', 'accepted');
        banner.classList.remove('is-visible');
      });
    }

    if (rejectBtn) {
      rejectBtn.addEventListener('click', function () {
        localStorage.setItem('cookieConsent', 'rejected');
        banner.classList.remove('is-visible');
      });
    }
  }

  // --- Contact form → WhatsApp ---
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();

      const nombre   = contactForm.querySelector('#nombre').value.trim();
      const empresa  = contactForm.querySelector('#empresa').value.trim();
      const email    = contactForm.querySelector('#email').value.trim();
      const telefono = contactForm.querySelector('#telefono').value.trim();
      const servicio = contactForm.querySelector('#servicio');
      const servicioTexto = servicio.options[servicio.selectedIndex].text !== '-- Selecciona una opción --'
        ? servicio.options[servicio.selectedIndex].text : '';
      const mensaje  = contactForm.querySelector('#mensaje').value.trim();

      let texto = '👋 *Nuevo contacto desde la web*\n\n';
      texto += '👤 *Nombre:* ' + nombre + '\n';
      if (empresa)      texto += '🏢 *Empresa:* ' + empresa + '\n';
      texto += '✉️ *Email:* ' + email + '\n';
      if (telefono)     texto += '📞 *Teléfono:* ' + telefono + '\n';
      if (servicioTexto) texto += '🔧 *Servicio:* ' + servicioTexto + '\n';
      texto += '\n💬 *Mensaje:*\n' + mensaje;

      const url = 'https://wa.me/34630381183?text=' + encodeURIComponent(texto);
      window.open(url, '_blank');
    });
  }

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // --- Intersection Observer for fade-in ---
  if ('IntersectionObserver' in window) {
    const style = document.createElement('style');
    style.textContent = '.fade-in { opacity: 0; transform: translateY(24px); transition: opacity 0.5s ease, transform 0.5s ease; } .fade-in.visible { opacity: 1; transform: none; }';
    document.head.appendChild(style);

    document.querySelectorAll('.service-card, .value-card, .stat-item, .testimonial-card, .why__feature').forEach(function (el) {
      el.classList.add('fade-in');
    });

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    document.querySelectorAll('.fade-in').forEach(function (el) { observer.observe(el); });
  }
});

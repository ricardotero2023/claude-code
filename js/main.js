/* =============================================
   ZONA INFORMÁTICA PONTEVEDRA - Main JS
   ============================================= */

document.addEventListener('DOMContentLoaded', function () {

  // --- Mobile nav toggle ---
  const toggle = document.getElementById('navToggle');
  const nav = document.getElementById('mainNav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      const open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open);
    });
    document.addEventListener('click', function (e) {
      if (!toggle.contains(e.target) && !nav.contains(e.target)) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // --- Active nav link ---
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.navbar__link').forEach(function (link) {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });

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

  // --- Contact form ---
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const successMsg = document.getElementById('formSuccess');
      const submitBtn = contactForm.querySelector('[type="submit"]');

      submitBtn.disabled = true;
      submitBtn.textContent = 'Enviando...';

      // Simulate send (replace with actual endpoint)
      setTimeout(function () {
        contactForm.reset();
        submitBtn.disabled = false;
        submitBtn.textContent = 'Enviar mensaje';
        if (successMsg) { successMsg.style.display = 'block'; }
        setTimeout(function () {
          if (successMsg) { successMsg.style.display = 'none'; }
        }, 6000);
      }, 1200);
    });
  }

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        if (nav) {
          nav.classList.remove('is-open');
          if (toggle) toggle.setAttribute('aria-expanded', 'false');
        }
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

/**
 * Navigation mobile et bouton de retour en haut de page.
 * Le script est chargé avec `defer` : les éléments HTML existent donc déjà.
 */

const scrollTopButton = document.querySelector('#scrollTopBtn');
const navigationToggle = document.querySelector('.nav-toggle');
const navigation = document.querySelector('#primary-navigation');

const scrollThreshold = 300;

/** Affiche le bouton après un court défilement pour ne pas encombrer l'accueil. */
function updateScrollTopButton() {
    const shouldShowButton = window.scrollY > scrollThreshold;
    scrollTopButton.classList.toggle('show', shouldShowButton);
}

/** Ouvre ou ferme le menu compact sur mobile. */
function toggleMobileNavigation() {
    const isOpen = navigationToggle.getAttribute('aria-expanded') === 'true';
    navigationToggle.setAttribute('aria-expanded', String(!isOpen));
    navigation.classList.toggle('is-open', !isOpen);
}

if (scrollTopButton) {
    window.addEventListener('scroll', updateScrollTopButton, { passive: true });
    updateScrollTopButton();

    scrollTopButton.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

if (navigationToggle && navigation) {
    navigationToggle.addEventListener('click', toggleMobileNavigation);

    navigation.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
            navigationToggle.setAttribute('aria-expanded', 'false');
            navigation.classList.remove('is-open');
        });
    });
}

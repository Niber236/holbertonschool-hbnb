// ==========================================
// BLOC DE DÉMARRAGE (Ce qui se lance au chargement des pages)
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    
    // === PARTIE 1 : GESTION DU LOGIN (Task 1) ===
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // === PARTIE 2 : GESTION DE LA PAGE D'ACCUEIL (Task 2) ===
    if (document.getElementById('places-list')) {
        checkAuthentication();
        setupFilter();
    }

    // === PARTIE 3 : GESTION DE LA PAGE DE DÉTAILS (Task 3) ===
    if (document.getElementById('place-details')) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            checkPlaceAuthentication(placeId);
        } else {
            document.getElementById('place-details').innerHTML = '<p>Place non trouvée (ID manquant).</p>';
        }
    }

    // === PARTIE 4 : GESTION DU FORMULAIRE D'AVIS (Task 4) ===
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const token = getCookie('token');
        // Le videur : pas de badge, retour à l'accueil
        if (!token) {
            window.location.href = 'index.html';
        } else {
            const placeId = getPlaceIdFromURL();
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const reviewText = document.getElementById('review-text').value;
                await submitReview(token, placeId, reviewText);
            });
        }
    }
});


// ==========================================
// TOUTES LES FONCTIONS
// ==========================================

// --- OUTIL GLOBAL ---
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// --- FONCTIONS DU LOGIN ---
async function loginUser(email, password) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        });
        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            alert('Login failed. Mauvais mot de passe ?');
        }
    } catch (error) {
        console.error('Erreur:', error);
    }
}

// --- FONCTIONS DE LA PAGE D'ACCUEIL ---
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
    }
    
    // On va chercher les données connectés ou pas
    fetchPlaces(token);
}

async function fetchPlaces(token) {
    try {
        const headers = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            // AJOUTE CETTE LIGNE POUR ESPIONNER LES DONNÉES :
            console.log("Voici ce que le backend m'envoie :", places); 
            displayPlaces(places);
        } else {
            console.error('Impossible de charger les lieux.');
        }
    } catch (error) {
        console.error('Erreur de connexion avec l\'API:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const card = document.createElement('article');
        card.className = 'place-card';
        card.dataset.price = place.price || 0; 
        
        card.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price || 'N/A'}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(card);
    });
}

function setupFilter() {
    const priceFilter = document.getElementById('price-filter');
    priceFilter.addEventListener('change', (event) => {
        const maxPrice = event.target.value;
        const cards = document.querySelectorAll('.place-card');

        cards.forEach(card => {
            const placePrice = parseFloat(card.dataset.price);
            if (maxPrice === 'All' || placePrice <= parseFloat(maxPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

// --- FONCTIONS DE LA PAGE DE DÉTAILS ---
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

function checkPlaceAuthentication(placeId) {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    const addReviewBtn = document.getElementById('add-review-btn');

    if (!token) {
        loginLink.style.display = 'block';
        addReviewSection.style.display = 'none';
        fetchPlaceDetails(null, placeId);
    } else {
        loginLink.style.display = 'none';
        addReviewSection.style.display = 'block';
        addReviewBtn.href = `add_review.html?id=${placeId}`; 
        fetchPlaceDetails(token, placeId);
    }
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            document.getElementById('place-details').innerHTML = '<p>Erreur: Impossible de charger les détails.</p>';
        }
    } catch (error) {
        console.error('Erreur API:', error);
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    
    const amenitiesList = place.amenities && place.amenities.length > 0
        ? place.amenities.map(a => a.name || a).join(', ')
        : 'Aucun équipement renseigné';

    let reviewsHtml = '';
    if (place.reviews && place.reviews.length > 0) {
        place.reviews.forEach(review => {
            reviewsHtml += `
                <article class="review-card">
                    <p>"${review.text}"</p>
                    <p><em>- ${review.user_id} (${review.rating}/5)</em></p>
                </article>
            `;
        });
    } else {
        reviewsHtml = '<p>Aucun avis pour le moment.</p>';
    }

    placeDetails.innerHTML = `
        <section class="place-info">
            <h1>${place.title}</h1>
            <p><strong>Host:</strong> ${place.owner_id}</p>
            <p><strong>Price per night:</strong> $${place.price || 'N/A'}</p>
            <p><strong>Description:</strong> ${place.description || 'Pas de description.'}</p>
            <p><strong>Amenities:</strong> ${amenitiesList}</p>
        </section>
        <section class="reviews">
            <h2>Reviews</h2>
            ${reviewsHtml}
        </section>
    `;
}

// --- FONCTION POUR AJOUTER UN AVIS (Task 4) ---
async function submitReview(token, placeId, reviewText) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ 
                place_id: placeId, 
                text: reviewText 
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const errorData = await response.json();
            alert('Failed to submit review: ' + (errorData.error || response.statusText));
        }
    } catch (error) {
        console.error('Erreur lors de l\'envoi de l\'avis:', error);
    }
}
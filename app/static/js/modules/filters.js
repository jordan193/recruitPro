// Gestion des filtres
export function initDynamicFilters() {
    const filterForm = document.getElementById('job-filter-form');
    if (filterForm) {
        const inputs = filterForm.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                // Vérifier et nettoyer les valeurs avant soumission
                inputs.forEach(inputField => {
                    if (inputField.value === 'None' || inputField.value.trim() === '') {
                        inputField.removeAttribute('name'); // Évite d'envoyer des valeurs inutiles
                    }
                });

                showLoadingIndicator(); // Afficher un indicateur de chargement
                filterForm.submit(); // Soumettre le formulaire
            });
        });
    }
}

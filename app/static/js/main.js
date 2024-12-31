// Point d'entrée principal
import { initFormValidation } from './modules/forms.js';
import { initDynamicFilters } from './modules/filters.js';
import { initJobCRUD } from './modules/jobCrud.js';
import { initAnimations } from './modules/animations.js';

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des modules
    initFormValidation();
    initDynamicFilters();
    initJobCRUD();
    initAnimations();
});
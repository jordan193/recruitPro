// Gestion CRUD des offres d'emploi
import { showConfirmDialog, showNotification } from './notifications.js';

export function initJobCRUD() {
    initDeleteJobs();
    initEditJobs();
}

function initDeleteJobs() {
    document.querySelectorAll('.delete-job-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            if (await showConfirmDialog('Êtes-vous sûr de vouloir supprimer cette offre ?')) {
                const jobId = btn.dataset.jobId;
                const card = document.querySelector(`#job-card-${jobId}`);
                
                try {
                    const response = await fetch(`/recruiter/job/${jobId}`, {
                        method: 'DELETE',
                        headers: { 'Content-Type': 'application/json' }
                    });
                    
                    if (response.ok) {
                        card.style.animation = 'slideOut 0.3s ease-out forwards';
                        setTimeout(() => card.remove(), 300);
                        showNotification('Offre supprimée avec succès', 'success');
                    }
                } catch (error) {
                    showNotification('Erreur lors de la suppression', 'error');
                }
            }
        });
    });
}

function initEditJobs() {
    document.querySelectorAll('.edit-job-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const jobId = btn.dataset.jobId;
            const jobCard = document.querySelector(`#job-card-${jobId}`);
            
            jobCard.querySelectorAll('.view-mode, .edit-mode').forEach(el => {
                el.style.animation = 'fade 0.3s ease-in-out';
                setTimeout(() => {
                    el.classList.toggle('d-none');
                    el.style.animation = '';
                }, 300);
            });
        });
    });
}
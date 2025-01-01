// Système de notifications
export function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} animate__animated animate__fadeInRight`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">×</button>
    `;
    
    document.body.appendChild(notification);
    
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.classList.replace('animate__fadeInRight', 'animate__fadeOutRight');
        setTimeout(() => notification.remove(), 300);
    });
    
    setTimeout(() => {
        notification.classList.replace('animate__fadeInRight', 'animate__fadeOutRight');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

export function showConfirmDialog(message) {
    return new Promise((resolve) => {
        const dialog = document.createElement('div');
        dialog.className = 'confirm-dialog animate__animated animate__fadeIn';
        dialog.innerHTML = `
            <div class="confirm-dialog-content">
                <p>${message}</p>
                <div class="confirm-dialog-buttons">
                    <button class="btn btn-secondary" data-result="false">Annuler</button>
                    <button class="btn btn-danger" data-result="true">Supprimer</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(dialog);
        
        dialog.querySelectorAll('button').forEach(button => {
            button.addEventListener('click', () => {
                const result = button.dataset.result === 'true';
                dialog.classList.replace('animate__fadeIn', 'animate__fadeOut');
                setTimeout(() => dialog.remove(), 300);
                resolve(result);
            });
        });
    });
}
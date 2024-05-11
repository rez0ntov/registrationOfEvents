document.addEventListener('DOMContentLoaded', function() {
    const linkButtons = document.querySelectorAll('.link');
    
    linkButtons.forEach(function(linkButton) {
        linkButton.addEventListener('click', function() {
            const link = this.getAttribute('data-link');
            
            navigator.clipboard.writeText(link).then(function() {
                alert('Ссылка скопирована в буфер обмена: ' + link);
            }).catch(function(err) {
                console.error('Не удалось скопировать ссылку: ', err);
            });
        });
    });
});

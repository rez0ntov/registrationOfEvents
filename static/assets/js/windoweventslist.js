document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');

    sidebar.addEventListener('click', function(e) {
        if (e.target.classList.contains('open_pop_up')) {
            const popUp = e.target.closest('.col-xxl-4').querySelector('.pop_up');
            popUp.classList.add('active');
        }

        if (e.target.classList.contains('pop_up_close')) {
            const popUp = e.target.closest('.pop_up');
            popUp.classList.remove('active');
        }
    });
});
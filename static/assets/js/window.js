document.addEventListener('DOMContentLoaded', function() {
    const openPopUps = document.querySelectorAll('.open_pop_up');
    const closePopUp = document.getElementById('pop_up_close');
    const popUp = document.getElementById('pop_up');

    openPopUps.forEach(openPopUp => {
        openPopUp.addEventListener('click', function (e){
            e.preventDefault();
            popUp.classList.add('active');
        });
    });

    closePopUp.addEventListener('click', () => { 
        popUp.classList.remove('active');
    });
});
var spanElement = document.getElementById('Id');
var idValue = spanElement.id;


fetch('/update_event', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id: idValue }),
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Ошибка:', error));


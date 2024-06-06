const toggle = document.getElementById('toggleDark');
const body = document.querySelector('body');
const card = document.querySelector('.card');
const savedMood = localStorage.getItem("mood");

// Si un état est trouvé, l'appliquer
if (savedMood === 'dark') {
    toggle.classList.add('bi-moon');
    body.style.background = 'rgb(7, 54, 74)';
    body.style.color = 'white';
    
   
} else {
    toggle.classList.remove('bi-moon');
    body.style.background = 'white';
    body.style.color = 'black';
   
}

toggle.addEventListener('click', function(){
    var mood = this.classList.toggle('bi-moon');
    // Sauvegarder l'état dans localStorage lors du clic
    localStorage.setItem("mood", mood ? 'dark' : 'light');

    if(mood){
        body.style.background = 'rgb(7, 54, 74)';
        body.style.color = 'white';
       
    } else {
        body.style.background = 'white';
        body.style.color = 'black';
    }
    body.style.transition = '2s';
});
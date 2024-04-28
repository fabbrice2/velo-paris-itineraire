document.addEventListener('DOMContentLoaded', function () {
    // Déconnexion lorsque l'utilisateur clique sur le S en haut à droite
    const disconnectButton = document.querySelector('.s');
    disconnectButton.addEventListener('click', function () {
      alert('Vous êtes déconnecté !');
      // Ici, vous pouvez ajouter le code pour la déconnexion réelle
    });
  
    // Rendre cliquable le header "Accueil" et "Favoris"
    const headerLinks = document.querySelectorAll('.accueil, .favoris');
    headerLinks.forEach(link => {
      link.addEventListener('click', function () {
        // Vous pouvez ajouter ici le code pour rediriger l'utilisateur vers les pages respectives
        alert(`Vous avez cliqué sur ${link.textContent}`);
      });
      // Effet de survol avec la couleur bleue fournie
      link.addEventListener('mouseover', function () {
        link.style.color = '#009eb5';
      });
      link.addEventListener('mouseout', function () {
        link.style.color = ''; // Retour à la couleur par défaut
      });
    });
  
    // Rendre cliquable les boutons "Favoris" et "Aucun Favoris" avec effet de survol
    const favorisButtons = document.querySelectorAll('.rectangle-button, .rectangle-button-2');
    favorisButtons.forEach(button => {
      button.addEventListener('click', function () {
        alert(`Vous avez cliqué sur ${button.textContent}`);
        // Vous pouvez ajouter ici le code pour afficher la liste des favoris ou effectuer d'autres actions
      });
      // Effet de survol avec la couleur bleue fournie
      button.addEventListener('mouseover', function () {
        button.style.backgroundColor = '#009eb5';
      });
      button.addEventListener('mouseout', function () {
        button.style.backgroundColor = ''; // Retour à la couleur par défaut
      });
    });
  }); // Accolade de fermeture manquante
  
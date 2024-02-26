// Confirmation de suppression avec fenêtre d'alerte
document.querySelectorAll('.delete-post').forEach(item => {
    item.addEventListener('click', event => {
        event.preventDefault();
        event.stopPropagation()
        const postId = item.getAttribute('data-post-id');
        const dataPostType = item.getAttribute('data-post-type');
        if (confirm('Voulez-vous vraiment supprimer ce post?')) {
            if (dataPostType === "ticket"){
                window.location.href = `/ticket/${postId}/delete`;
            }
            else if(dataPostType === "review"){
                window.location.href = `/review/${postId}/delete`;
            }; 
           
        }
    });
});
function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}


function submit_edit(id){
    const txtarea_value = document.getElementById(`textarea_${id}`).value
    const content = document.getElementById(`content_${id}`);
    const modal = document.getElementById(`modal_edit_post_${id}`);
    fetch(`/edit/${id}`,{
      method: "POST",
      headers: {"content-type" : "application/json", "X-CSRFToken" : getCookie("csrftoken")},
      body: JSON.stringify({
        content : txtarea_value
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      content.innerHTML = result.data;

       // on the modal change state like in hidden modal
      modal.classList.remove('show');
      modal.setAttribute('aria-hidden', 'true');
      modal.setAttribute('style', 'display: none');

      // get modal backdrop
      const modalsBackdrop = document.getElementsByClassName('modal-backdrop');

      // remove modal backdrop
      document.body.removeChild(modalsBackdrop[0]);

    });
  }
  
function likeHandler(id, posts_Liked ){
    const btn = document.getElementById(`${id}`);
    const isHeartFilled = btn.classList.contains('bi','bi-heart-fill');

    console.log('Button:', btn);
    console.log('Is Heart Filled:', isHeartFilled);

    btn.classList.remove('bi-heart-fill', 'bi-heart');

    if(posts_Liked.indexOf(id) >= 0){
      var liked = true;
    }
    else{
      var liked = false;
    }

    if(liked === true){
      fetch(`/remove_like/${id}`)
      .then(response => response.json())
      .then(result => {
        console.log('Remove Like Result:', result);
        console.log(result.message);
        btn.classList.remove('btn', 'btn-danger');
        // Remove 'bi-heart-fill' class and add 'bi-heart' class
        btn.classList.remove('bi-heart-fill');
        // Changing the like icon and button color
        btn.innerHTML = liked? "bi bi-heart" : "bi bi-heart-fill";
        btn.classList = liked? "btn btn-primary" : "btn btn-danger";
        //change like state
        liked = false;

        console.log('liked state:' ,liked)
      });
    }
    else{
      fetch(`/add_like/${id}`)
      .then(response => response.json())
      .then(result => {
        console.log('Add Like Result:', result);
        console.log(result.message);
        btn.classList.remove('btn', 'btn-primary');
        // Remove 'bi-heart' class and add 'bi-heart-fill' class
        btn.classList.remove('bi-heart');
        // Changing the like icon and button color
        btn.innerHTML = liked? "bi bi-heart-fill" : "bi bi-heart";
        btn.classList = liked? "btn btn-danger" : "btn btn-primary";
        //change like state
        liked = true;

        console.log('liked state: ',liked)
      }); 
    }
    
 }

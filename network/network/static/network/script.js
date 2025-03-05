document.addEventListener('DOMContentLoaded', function () {
    // Dodawanie nowego posta
    const newPostForm = document.getElementById("new-post-form");
    if (newPostForm) {
        newPostForm.addEventListener("submit", function(event) {
            event.preventDefault();

            let content = document.getElementById("post-content").value;

            fetch(createPostUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken 
                },
                body: `content=${encodeURIComponent(content)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert("Post published!");
                    location.reload();  
                } else {
                    alert("Error: " + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Error occurred");
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.dataset.postId;
            const postContent = document.getElementById(`post-content-${postId}`);
            const postDiv = postContent.closest('.post');
            this.style.display = 'none';

            const editForm = postDiv.querySelector('.edit-form');
            editForm.style.display = 'block';

            editForm.addEventListener('submit', function (e) {
                e.preventDefault();
                const editedContent = editForm.querySelector('textarea').value;

                fetch(`/edit_post/${postId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken 
                    },
                    body: JSON.stringify({ content: editedContent })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Server error: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        postContent.innerText = editedContent;
                        postContent.style.display = 'block';
                        editForm.style.display = 'none';

                        button.style.display = 'inline-block';
                    } else {
                        alert("Error editing post.");
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.dataset.postId;
            const icon = this.querySelector('i');
            const likeCount = this.querySelector('.like-count');
            const liked = icon.classList.contains('fa-heart-broken'); 

            fetch(`/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken, 
                },
                body: JSON.stringify({ liked: !liked })  
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (liked) {
                        icon.classList.remove('fa-heart-broken');
                        icon.classList.add('fa-heart');
                    } else {
                        icon.classList.remove('fa-heart');
                        icon.classList.add('fa-heart-broken');
                    }
                    likeCount.innerText = data.new_like_count;
                } else {
                    alert('You are not logged in');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('You are not logged in');
            });
        });
    });
});
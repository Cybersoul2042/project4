document.addEventListener("DOMContentLoaded", function(){
    document.getElementById('all-posts').addEventListener('click', () => PostsTypes('AllPosts'));
    document.querySelector('.new-tweet-form').addEventListener('submit', event => {
        event.preventDefault();
        Post();
    });

    PostsTypes('AllPosts')
});

function PostsTypes(postTypes){

    document.querySelector('.all-posts').style.display = 'block';

    document.querySelector('h2').innerHTML = `${postTypes}`

    fetch('/tweets/' + postTypes)
    .then(response => response.json())
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.log('Error :', error);
    })

}

function Post(){

    fetch('/tweets',{
        method: 'POST',
        body: JSON.stringify({
            post: document.querySelector('#post-text').value
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        alert('Error :', error);
    });
}
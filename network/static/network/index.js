document.addEventListener("DOMContentLoaded", function() {

    document.querySelector('#allposts').addEventListener('click', () => PostsTypes('allposts', 'All Posts'));
    document.querySelector('#user').addEventListener('click', () => PostsTypes('myposts', 'My Posts'));
    document.querySelector('#newpost').addEventListener('click', () => newPost());

    PostsTypes('allposts', 'All Posts');
    
});

function PostsTypes(posttype, name)
{
    let currentPosts;
    if(posttype === 'allposts')
    {
        currentPosts = document.querySelector('#all-posts');
        document.querySelector('#all-posts').style.display = 'block';
        document.querySelector('#follower-posts').style.display = 'none';
        document.querySelector('#my-posts').style.display = 'none';
        document.querySelector('#myModal').style.display = 'none';
    }
    else if(posttype === 'myposts')
    {
        currentPosts = document.querySelector('#my-posts');
        document.querySelector('#my-posts').style.display = 'block';
        document.querySelector('#follower-posts').style.display = 'none';
        document.querySelector('#all-posts').style.display = 'none';
        document.querySelector('#myModal').style.display = 'none';
    }
    else
    {
        currentPosts = document.querySelector('#follower-posts');
        document.querySelector('#follower-posts').style.display = 'block';
        document.querySelector('#all-posts').style.display = 'none';
        document.querySelector('#my-posts').style.display = 'none';
        document.querySelector('#myModal').style.display = 'none';
    }

    document.querySelector('h2').innerHTML = `${name}`;

    fetch('/tweets/' + posttype)
    .then(response => response.json())
    .then(tweets => {
        if(!tweets.length)
        {
            let tPlace = document.createElement('div');
            tPlace.setAttribute('id', 'no-post');
            tPlace.innerHTML = 'No posts yet!!'
            document.querySelector('#posts').appendChild(tPlace);
        }
        else
        {   
            let postsCont = document.createElement('div')
            postsCont.setAttribute('class', 'post')

            

            tweets.forEach(tweet => {
                
                let postCont = document.createElement('div')
                postCont.setAttribute('id', 'post-contents')

                postCont.innerHTML =`<div class="content1">
                                         
                                        <p id="sender">By: ${tweet['sender']}</p>
                                        <p id="text">${tweet['post']}</p>
                                         
                                     </div>
                                     <div class="content2">
                                        <div id="like-cont">
                                            <p>${tweet['likes']}</p>
                                        </div>
                                        <div id"date-cont">
                                            <p id="date">${tweet['tweetDate']}</p>
                                        </div>
                                     </div>`

                postsCont.append(postCont)
            });

            currentPosts.innerHTML = postsCont.outerHTML
            
        }
    })

}

function newPost(){
    
    let modal = document.getElementById("myModal");

    modal.style.display = 'block';

    window.onclick = function(event) {
        if (event.target == modal) {
           modal.style.display = 'none';
        }
    }  

    document.querySelector('form').addEventListener('submit', () => Post())
    
    
    
}

function Post(){
    let post = document.querySelector('#post-text').value;
    if(post.trim().length === 0)
    {
        alert('Please fill The post text')
        return 1;
    }
    else
    {
        fetch('/tweets',{
            method: 'POST',
            body: JSON.stringify({
                post: post
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
}

function like(id, currentLikes, isLiked){
    console.log('liked tweet : ', id);

    if(isLiked === false)
    {
        alert('liked')

        fetch('/tweets/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                likes: currentLikes + 1,
                isLiked: true
            }) 
        })
        .then(() => {
            window.location.reload()
        })
        .catch(error => {
            console.log('Error:', error);
        });z
    }
    else
    {
        alert('No liked')

        fetch('/tweets/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                likes: currentLikes - 1,
                isLiked: false
            }) 
        })
        .then(() => {
            window.location.reload()
        })
        .catch(error => {
            console.log('Error:', error);
            r
        });

    }
    
}
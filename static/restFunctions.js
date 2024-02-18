const host = 'localhost:5000';
var username = null;

function setUsername(name) {
    username = name;
}

function registerUser() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var email = document.getElementById("email").value;

    const requestData = {
        email: email, username: username, password: password
    }
    const requestOptions = {
        method: "POST", headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(requestData)
    }
    console.log("sending request to server");
    fetch("http://" + host + "/api/register", requestOptions)
        .then(res => {
            return res.json();
        })
        .then(data => {
            console.log("response: ", data['message']);
        })
        .catch(err => {
            console.log("usao u catch");
            console.log("Error: ", err);
        });
}

async function toggleLike(username, postID) {
    var requestData = {
        username: username, postID: postID
    }
    var requestOptions = {
        method: "POST", headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(requestData)
    }
    fetch("http://" + host + "/api/likes/toggle", requestOptions)
        .then(res => {
            return res.json();
        })
        .then(data => {
            console.log("response: ", data['message']);
        })
        .catch(err => {
            console.log("usao u catch");
            console.log("Error: ", err);
        });
}

function showPosts(limit) {
    return fetch('http://' + host + '/api/posts/all?limit=' + limit)
        .then(res => res.json())
        .then(async res => {
            //console.log(res);
            var userPostsDiv = document.getElementById('userPosts');
            while (userPostsDiv.firstChild) {
                userPostsDiv.removeChild(userPostsDiv.firstChild);
            }
            for (const resKey in res) {
                var post = res[resKey];
                //console.log(post);
                var newPostDiv = document.createElement("div");
                var pUsername = document.createElement("p");
                pUsername.textContent = post.author.username;
                var pDate = document.createElement("p");
                pDate.textContent = post['datetime'];
                var pContent = document.createElement("p");
                //console.log(post['content']);
                pContent.innerHTML = post['content'].replaceAll("\r\n", "<br>");
                newPostDiv.appendChild(pUsername);
                newPostDiv.appendChild(pDate);
                newPostDiv.appendChild(pContent);


                // var likeButton = document.createElement("button");
                // likeButton.setAttribute("value", "like post");
                // likeButton.textContent = "like post";
                // //likeButton.setAttribute("id", "likeButton");
                // likeButton.setAttribute("data-post-id", post['id'] + "");

                async function like(event) {
                    //var btn = document.getElementById("likeButton");
                    var btn = event.target;
                    var postID = btn.getAttribute("data-post-id");
                    postID = parseInt(postID);

                    if (btn.src.includes("like_img.png")) {
                        console.log("Changing image to active");
                        btn.src = "static/like_active.png";
                        btn.width = 25;
                        btn.height = 25;
                        console.log("liked post with id: ", postID);

                    } else if (btn.src.includes("like_active.png")) {
                        console.log("Changing image to default");
                        btn.src = "static/like_img.png";
                        btn.width = 30;
                        btn.height = 30;
                        // You can add logic here for unliking if needed
                    }
                    await toggleLike(username, postID);
                    var label = document.getElementById('label-for-post-' + postID);
                    label.textContent = await countLikesForPost(postID) + "";
                }

                // likeButton.addEventListener("click", like);
                // newPostDiv.appendChild(likeButton);

                var postLiked = await checkPostLiked(username, post['id']);
                //console.log("post liked:", post['id'], postLiked);

                var likeImg = document.createElement("img");
                likeImg.setAttribute("data-post-id", post['id'] + "");
                if (postLiked) {
                    likeImg.src = 'static/like_active.png';
                    likeImg.width = 25;
                    likeImg.height = 25;
                } else {
                    likeImg.src = 'static/like_img.png';
                    likeImg.width = 30;
                    likeImg.height = 30;
                }
                likeImg.addEventListener("click", like);
                likeImg.style.cursor = 'pointer';
                newPostDiv.appendChild(likeImg);

                var label = document.createElement("label");
                label.setAttribute("id", "label-for-post-" + post['id']);
                label.textContent = await countLikesForPost(post['id']) + "";
                newPostDiv.appendChild(label);

                if (pUsername.textContent === username) {
                    var delBtn = document.createElement("button");
                    delBtn.textContent = "delete post";
                    delBtn.setAttribute("data-post-id", post['id'] + "");
                    delBtn.addEventListener("click", deletePost);
                    newPostDiv.appendChild(delBtn);
                }

                document.getElementById("userPosts").appendChild(newPostDiv);
                document.getElementById("userPosts").appendChild(document.createElement("hr"));
            }
            //console.log(res.length);
            return res.length;
        })
        .catch(err => {
            console.log(err);
            return null;
        });
}

async function deletePost(event) {
    console.log("deleting")
    var btn = event.target;
    var postID = btn.getAttribute("data-post-id");
    var requestData = {
        username: username, postID: postID
    }
    var requestOptions = {
        method: "DELETE", headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(requestData)
    }
    await fetch("http://" + host + "/api/posts/delete", requestOptions)
        .then(res => {
            console.log(res);
            return res.json();
        })
        .then(data => {
            console.log("response: ", data['message']);
        })
        .catch(err => {
            console.log("usao u catch");
            console.log("Error: ", err);
        });
    window.location.reload();
}

async function getLikesForPost(postID) {
    try {
        var response = await fetch("http://" + host + "/api/likes/post/" + postID);
        // console.log(`response for ${postID}:`);
        // console.log(response);
        var data = await handleErrors(response);
        //console.log(data);
        return data;
    } catch (error) {
        console.error('Error getting likes for post:', error.message);
    }
}

const handleErrors = (response) => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
};

async function checkPostLiked(username, postID) {
    var likes = await getLikesForPost(postID);
    // console.log("likes in check:", postID);
    // console.log(likes);
    for (const likesKey in likes) {
        var like = likes[likesKey];
        // console.log("in for loop:", postID);
        // console.log(like);
        if (like.user.username === username) return true;
    }
    return false;
}

async function countLikesForPost(postID) {
    var likes = await getLikesForPost(postID);
    //console.log(likes.length);
    return likes.length;
}
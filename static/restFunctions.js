const host = 'localhost:5000';

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
    fetch("http://" + host + "/api/registerUser", requestOptions)
        .then(res => {
            return res.json();
        })
        .then(data => {
            console.log("response: ", data['message']);
        })
        .catch(err => {
            console.log("usao u catch");
            console.log("Error: ", err);
        })
}

function showPosts(limit) {
    return fetch('http://' + host + '/api/getPosts?limit=' + limit)
        .then(res => res.json())
        .then(res => {
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
                pUsername.textContent = post['authorUsername'];
                var pDate = document.createElement("p");
                pDate.textContent = post['datetime'];
                var pContent = document.createElement("p");
                //console.log(post['content']);
                pContent.innerHTML = post['content'].replaceAll("\r\n", "<br>");
                newPostDiv.appendChild(pUsername);
                newPostDiv.appendChild(pDate);
                newPostDiv.appendChild(pContent);
                var likeButton = document.createElement("button");
                likeButton.setAttribute("value", "like post");
                likeButton.textContent = "like post";
                //likeButton.setAttribute("id", "likeButton");
                likeButton.setAttribute("data-post-id", post['id'] + "");

                function like(event) {
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
                }

                likeButton.addEventListener("click", like);
                newPostDiv.appendChild(likeButton);

                var likeImg = document.createElement("img");
                likeImg.setAttribute("data-post-id", post['id'] + "");
                likeImg.src = 'static/like_img.png';
                likeImg.addEventListener("click", like);
                likeImg.width = 30;
                likeImg.height = 30;
                likeImg.style.cursor = 'pointer';
                newPostDiv.appendChild(likeImg);
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
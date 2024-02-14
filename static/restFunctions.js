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
    fetch('http://' + host + '/api/getPosts?limit=' + limit)
        .then(res => res.json())
        .then(res => {
            //console.log(res);
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
                document.getElementById("userPosts").appendChild(newPostDiv);
                document.getElementById("userPosts").appendChild(document.createElement("hr"));
            }
        })
        .catch(err => console.log(err));
}
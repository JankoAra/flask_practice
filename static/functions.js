import {
    getAllPosts,
    deletePost,
    toggleLike,
    getImageUrl,
    createPost,
    getAllUsers
} from "./jsAPICalls.js"

const inactiveLikeImgUrl = '/static/img/like_48.png';
const activeLikeImgUrl = '/static/img/like_GS_48.png';
const emptyProfileImage = "/static/img/empty_profile_image.png";
let sessionUsername = "";


export function setSessionUsername(name) {
    sessionUsername = name;
}

function createDefaultImage(imgW, imgH) {
    const imgElem = document.createElement("img");
    imgElem.src = emptyProfileImage;
    imgElem.alt = "User image";
    imgElem.width = imgW;
    imgElem.height = imgH;
    imgElem.style.objectFit = "contain";
    return imgElem;
}

export function createImageElement(imageUrl, imgW, imgH) {
    const imgElem = document.createElement("img");
    imgElem.src = imageUrl;
    imgElem.alt = "User image";
    imgElem.width = imgW;
    imgElem.height = imgH;
    imgElem.style.objectFit = "contain";
    return imgElem;
}

async function clickLikeButton(event) {
    const btn = event.target;
    let postID = btn.getAttribute("data-post-id");
    postID = parseInt(postID);
    const label = document.getElementById('label-for-post-' + postID);
    let numOfLikes = parseInt(label.textContent, 10);
    if (btn.src.includes(inactiveLikeImgUrl)) {
        console.log("Changing image to active");
        btn.src = activeLikeImgUrl;
        console.log("liked post with id: ", postID);
        numOfLikes++;
    } else if (btn.src.includes(activeLikeImgUrl)) {
        console.log("Changing image to default");
        btn.src = inactiveLikeImgUrl;
        numOfLikes--;
    }
    await toggleLike(sessionUsername, postID);
    label.textContent = numOfLikes.toString();
}

async function deletePostEvent(event) {
    const btn = event.target;
    const postID = btn.getAttribute("data-post-id");
    await deletePost(sessionUsername, postID);
    const div = document.getElementById('div-post-id-' + postID);
    div.innerHTML = "<p>Post deleted</p>";
}

async function buildPostDiv(post) {
    const div = document.createElement("div");
    div.setAttribute("id", 'div-post-id-' + post.id);
    const imageUrl = await getImageUrl(post.author.username);
    const imgW = 50;
    const imgH = 50;
    let img = (imageUrl === null) ? createDefaultImage(imgW, imgH) : createImageElement(imageUrl, imgW, imgH);
    img.classList.add("postUserImage");
    const username = document.createTextNode(post.author.username);
    const datetime = document.createTextNode(post.datetime);
    const content = document.createElement("p");
    content.innerHTML = post.content.replaceAll("\r\n", "<br>");

    const likeButton = document.createElement("img");
    likeButton.setAttribute("data-post-id", post.id);
    let postLiked = false;
    if (post.numOfLikes > 0) {
        for (let i = 0; i < post.likes.length; i++) {
            let l = post.likes[i];
            if (l.user.username === sessionUsername) {
                postLiked = true;
                break;
            }
        }
    }
    if (postLiked) {
        likeButton.src = activeLikeImgUrl;
    } else {
        likeButton.src = inactiveLikeImgUrl;
    }
    likeButton.width = 30;
    likeButton.height = 30;
    likeButton.style.cursor = "pointer";
    likeButton.addEventListener("click", clickLikeButton);

    const label = document.createElement("label");
    label.setAttribute("id", "label-for-post-" + post['id']);
    label.textContent = post.numOfLikes;

    div.appendChild(img);
    div.appendChild(username);
    div.appendChild(datetime);
    div.appendChild(content);
    div.appendChild(likeButton);
    div.appendChild(label);

    if (post.author.username === sessionUsername) {
        const delBtn = document.createElement("button");
        delBtn.textContent = "delete post";
        delBtn.setAttribute("data-post-id", post['id'] + "");
        delBtn.addEventListener("click", deletePostEvent);
        div.appendChild(delBtn);
    }

    return div;
}

export async function showPosts(limit, offset) {
    const userPostsDiv = document.getElementById('userPosts');
    const postsData = await getAllPosts(limit, offset);
    for (const postsDataKey in postsData) {
        const post = postsData[postsDataKey];
        const newPostDiv = await buildPostDiv(post);

        userPostsDiv.appendChild(newPostDiv);
        userPostsDiv.appendChild(document.createElement("hr"));
    }
    return postsData.length;
}

export async function submitPost() {
    const textArea = document.getElementById("postContent");
    const content = textArea.value;
    if (!content) {
        console.log("Post content is empty. No post created.");
        return;
    }
    const newPost = await createPost(sessionUsername, content);
    const newPostDiv = await buildPostDiv(newPost);
    const userPostsDiv = document.getElementById("userPosts");
    let dataLimit = parseInt(userPostsDiv.getAttribute("data-limit"), 10);
    dataLimit++;
    userPostsDiv.setAttribute('data-limit', dataLimit.toString());
    userPostsDiv.insertAdjacentElement("afterbegin", document.createElement("hr"));
    userPostsDiv.insertAdjacentElement("afterbegin", newPostDiv);
    // userPostsDiv.innerHTML = "";
    // await showPosts(dataLimit, 0);
    textArea.value = "";
}

export async function showProfileImage() {
    const imgW = 200;
    const imgH = 200;
    const imageUrl = await getImageUrl(sessionUsername);
    let img = (imageUrl === null) ? createDefaultImage(imgW, imgH) : createImageElement(imageUrl, imgW, imgH);
    img.setAttribute("id", "profileImage");
    document.getElementById("mainImage").appendChild(img);
}

export async function loadMorePosts() {
    const userPostsDiv = document.getElementById("userPosts");
    let currentLimit = userPostsDiv.getAttribute("data-limit");
    currentLimit = parseInt(currentLimit, 10);
    const newPostsToLoad = 8;
    const newLimit = currentLimit + newPostsToLoad;
    userPostsDiv.setAttribute('data-limit', newLimit.toString());
    const postsReturned = await showPosts(newPostsToLoad, currentLimit);
    if (postsReturned < newPostsToLoad) {
        document.getElementById("loadMorePostsLink").remove();
        const msg = document.createElement("p");
        msg.textContent = "All posts loaded!";
        userPostsDiv.insertAdjacentElement("afterend", msg);
    }
}

export async function showUsers() {
    const userList = document.getElementById('userList');

    if (userList.style.display === 'none' || userList.style.display === '') {
        const userData = await getAllUsers();
        const usersListContent = document.getElementById('usersListContent');
        usersListContent.innerHTML = '<p>All users</p>';  // Clear existing content


        // Display each username one per line
        userData.forEach(function (user) {
            let li = document.createElement('li');
            li.textContent = user.username;
            usersListContent.appendChild(li);
        });

        // Show the user list
        userList.style.display = 'block';
    } else {
        // If the user list is already visible, hide it
        userList.style.display = 'none';
    }
}

export function togglePassword() {
    const passwordField = document.getElementById("password");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

export async function setFlaskSessionUsername(username) {
    await fetch(`/session/username/${username}`, {method: "POST"});
}
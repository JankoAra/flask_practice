import {
    registerUser,
    getUserByUsername,
    getUserById,
    getAllUsers,
    getAllPosts,
    getAllPostsForUsername,
    createPost,
    deletePost,
    toggleLike,
    getLikesForPost,
    createPoke,
    getPokesForUsername,
    getPokesForUserID,
    readPoke,
    getImageUrl
} from "./jsAPICalls.js"

const inactiveLikeImgUrl = '/static/img/like_48.png';
const activeLikeImgUrl = '/static/img/like_GS_48.png';
var sessionUsername = "";


export function setSessionUsername(name) {
    sessionUsername = name;
}

export function createDefaultImage(imgW, imgH) {
    const imgElem = document.createElement("img");
    imgElem.src = "/static/img/empty_profile_image.png";
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

async function like(event) {
    const btn = event.target;
    let postID = btn.getAttribute("data-post-id");
    postID = parseInt(postID);
    const label = document.getElementById('label-for-post-' + postID);
    let num2 = parseInt(label.textContent, 10);
    if (btn.src.includes(inactiveLikeImgUrl)) {
        console.log("Changing image to active");
        btn.src = activeLikeImgUrl;
        console.log("liked post with id: ", postID);
        num2++;

    } else if (btn.src.includes(activeLikeImgUrl)) {
        console.log("Changing image to default");
        btn.src = inactiveLikeImgUrl;
        num2--;
    }
    await toggleLike(username, postID);
    label.textContent = num2.toString();
}

async function deletePostEvent(event) {
    const btn = event.target;
    const postID = btn.getAttribute("data-post-id");
    await deletePost(username, postID);
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
            if (l.user.username === username) {
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
    likeButton.addEventListener("click", like);

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
    var userPostsDiv = document.getElementById('userPosts');
    //userPostsDiv.innerHTML = "";

    var postsData = await getAllPosts(limit, offset);
    for (const postsDataKey in postsData) {
        const post = postsData[postsDataKey];
        const newPostDiv = await buildPostDiv(post);

        userPostsDiv.appendChild(newPostDiv);
        userPostsDiv.appendChild(document.createElement("hr"));
    }
    return postsData.length;
}
// Function to handle errors and display messages
function handleErrors(response) {
    if (!response.ok) {
        return {error: `Request failed with status ${response.status}`};
    }
    return response.json();
}

// Function to register a new user
async function registerUser(username, email, password) {
    try {
        const response = await fetch('/api/users/register', {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
            }, body: JSON.stringify({
                username: username, email: email, password: password,
            }),
        });
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error registering user:', data.error);
        } else {
            console.log('User registered successfully:', data);
        }
        return data;
    } catch (error) {
        console.error('Error registering user:', error.message);
        return {error: error.message};
    }
}

// Function to get user by username
async function getUserByUsername(username) {
    try {
        const encodedUsername = encodeURIComponent(username);
        const response = await fetch(`/api/users/getByUsername/${encodedUsername}`);
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error getting user:', data.error);
        } else {
            console.log('User:', data);
        }
        return data;
    } catch (error) {
        console.error('Error getting user by username:', error.message);
        return {error: error.message};
    }
}

// Function to get user by ID
async function getUserById(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error getting user by ID:', data.error);
        } else {
            console.log('User data:', data);
        }
        return data;
    } catch (error) {
        console.error('Error getting user by ID:', error.message);
        return {error: error.message};
    }
}

// Function to get all users
async function getAllUsers() {
    try {
        const response = await fetch('/api/users/all');
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error getting all users:', data.error);
        } else {
            console.log('All users:', data);
        }
        return data;
    } catch (error) {
        console.error('Error getting all users:', error.message);
        return {error: error.message};
    }
}

// Function to get all posts
async function getAllPosts(limit) {
    try {
        const response = await fetch('/api/posts/all?limit=' + limit);
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error getting all posts:', data.error);
        } else {
            console.log('All posts:', data);
        }
        return data;
    } catch (error) {
        console.error('Error getting all posts:', error.message);
        return {error: error.message};
    }
}

// Function to get all posts for a specific username
async function getAllPostsForUsername(username) {
    try {
        const encodedUsername = encodeURIComponent(username);
        const response = await fetch(`/api/posts/${encodedUsername}`);
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error getting posts for username:', data.error);
        } else {
            console.log(`All posts for ${username}:`, data);
        }
        return data;
    } catch (error) {
        console.error('Error getting posts for username:', error.message);
        return {error: error.message};
    }
}

// Function to create a new post
async function createPost(username, content) {
    try {
        const response = await fetch('/api/posts/new', {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
            }, body: JSON.stringify({
                username: username, content: content,
            }),
        });
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error creating post:', data.error);
        } else {
            console.log('Post created successfully:', data);
        }
        return data;
    } catch (error) {
        console.error('Error creating post:', error.message);
        return {error: error.message};
    }
}

// Function to delete a post
async function deletePost(username, postID) {
    try {
        const response = await fetch('/api/posts/delete', {
            method: 'DELETE', headers: {
                'Content-Type': 'application/json',
            }, body: JSON.stringify({
                username: username, postID: postID,
            }),
        });
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error deleting post:', data.error);
        } else {
            console.log('Post deleted:', data);
        }
        return data;
    } catch (error) {
        console.error('Error deleting post:', error.message);
        return {error: error.message};
    }
}

// Function to toggle like for a post
async function toggleLike(username, postID) {
    try {
        const response = await fetch('/api/likes/toggle', {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
            }, body: JSON.stringify({
                username: username, postID: postID,
            }),
        });
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error toggling like:', data.error);
        } else {
            console.log('Like toggled:', data);
        }
        return data;
    } catch (error) {
        console.error('Error toggling like:', error.message);
        return {error: error.message};
    }
}

// Function to get likes for a post
async function getLikesForPost(postID) {
    try {
        const response = await fetch(`/api/likes/post/${postID}`);
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error getting likes for post:', data.error);
        } else {
            console.log(`Likes for post ${postID}:`, data);
        }
        return data;
    } catch (error) {
        console.error('Error getting likes for post:', error.message);
        return {error: error.message};
    }
}

async function getPokesForUserID(userID) {
    try {
        const response = await fetch(`/api/pokes/user/${userID}`);
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error getting pokes for user:', data.error);
        } else {
            console.log(`Pokes for user ${userID}:`, data);
        }
        return data;
    } catch (error) {
        console.error('Error getting pokes for user:', error.message);
        return {error: error.message};
    }
}

async function getPokesForUsername(username) {
    try {
        const response = await fetch(`/api/pokes/username/${username}`);
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error getting pokes for username:', data.error);
        } else {
            console.log(`Pokes for username ${username}:`, data);
        }
        return data;
    } catch (error) {
        console.error('Error getting pokes for username:', error.message);
        return {error: error.message};
    }
}

async function createPoke(usernamePoking, usernamePoked) {
    try {
        const response = await fetch('/api/pokes/new', {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
            }, body: JSON.stringify({
                usernamePoking: usernamePoking, usernamePoked: usernamePoked,
            }),
        });
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error creating poke:', data.error);
        } else {
            console.log('Poke created:', data);
        }
        return data;
    } catch (error) {
        console.error('Error creating poke:', error.message);
        return {error: error.message};
    }
}

async function readPoke(pokeID) {
    try {
        const response = await fetch('/api/pokes/read/' + pokeID, {
            method: 'PUT'
        });
        const data = handleErrors(response);
        if (data.error) {
            console.error('Error reading poke:', data.error);
        } else {
            console.log('Poke status changed:', data);
        }
        return data;
    } catch (error) {
        console.error('Error reading poke:', error.message);
        return {error: error.message};
    }
}

async function getImage(username, imageContainer, imgSize) {
    await fetch(`/api/users/images/${username}`)
        .then(response => response.json())
        .then(data => {
            while(imageContainer.firstChild){
                imageContainer.removeChild(imageContainer.firstChild);
            }
            if (data.error) {
                //imageContainer.innerHTML = `<p>${data.error}</p>`;
                const imgElem = document.createElement("img");
                imgElem.src = "/static/img/empty_profile_image.png";
                imgElem.alt = "User image";
                imgElem.width = imgSize;
                imgElem.height = imgSize;
                imgElem.style.objectFit = "contain";
                imageContainer.appendChild(imgElem);
            } else {
                const imageData = data.image;
                const imageUrl = `data:image/png;base64,${imageData}`;

                const imgElem = document.createElement("img");
                imgElem.src = imageUrl;
                imgElem.alt = "User image";
                imgElem.width = imgSize;
                imgElem.height = imgSize;
                imgElem.style.objectFit = "contain";
                imageContainer.appendChild(imgElem);
            }
        })
        .catch(error => console.error('Error:', error));
}
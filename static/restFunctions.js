function registerUser() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var email = document.getElementById("email").value;

    const requestData = {
        email: email,
        username: username,
        password: password
    }
    const requestOptions = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    }
    console.log("sending request to server");
    fetch("http://localhost:5000/api/registerUser", requestOptions)
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
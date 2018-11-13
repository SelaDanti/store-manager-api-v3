let loginUrl = 'http://storemanage3000.herokuapp.com/api/v2/auth/activate'
let activateInfo = `
<div class="center">
    <img src="images/profile.png" alt="Profile">
    <h1>Account has been activated</h1>
    <a href="index.html" class="btn-main"> Login</a><br><br>
</div>
`

document.getElementById('submit-login').addEventListener('click',login)

function login(){
    let firstName = document.getElementById("first-name").value;
    let lastName = document.getElementById("last-name").value;
	let email = document.getElementById("email").value;
	let password = document.getElementById("password").value;
    let key = document.getElementById("key").value;
	let payload = {
  "email": email,
  "first name": firstName,
  "last name": lastName,
  "password": password,
  "activation key": key
}
	fetch(loginUrl,{
				"method": "POST",
				"mode":"cors",
				headers: {
			      "Content-type": "application/json",
			      "Access-Control-Allow-Origin":"*"
			    },
			    body: JSON.stringify(payload)
	})
    .then((res) => {
    	status = res.status;
        return res.json();
    })
    .then((data)=>{
        if (status != 201)
        {
            document.getElementById('error').innerHTML = data.error;
            document.getElementById('error').style.display = 'block';
        }
        else
        {
            document.getElementsByClassName('login-box')[0].innerHTML = activateInfo;
        }
    })
    .catch((error) => {console.log(error);});
}
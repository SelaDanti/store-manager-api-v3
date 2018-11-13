attendantUrl = `http://storemanage3000.herokuapp.com/api/v2/attendants`

document.getElementsByClassName('btn-main')[0].addEventListener("click", myFunction);

function myFunction() {
    let firstName = document.getElementById('firstName').value;
    let lastName = document.getElementById('lastName').value;
    let email = document.getElementById('email').value;
    let role = document.getElementById('role').value;
    let password = document.getElementById('password').value;
    let payload = {
  "last name": lastName,
  "email": email,
  "user type": role,
  "password": password,
  "first name": firstName
};
    fetch(attendantUrl,{
    	"method":"POST",
    	"mod":"cors",
    	headers: {
		"Content-type": "application/json",
		"Access-Control-Allow-Origin":"*",
		"X-API-KEY": localStorage.getItem('token')
    	},
    	body:JSON.stringify(payload)
    })
    .then((res) => {status = res.status; return res.json()})
    .then((data) => {
    	if (status != 201)
    	{
            if (data['error'] == 'token is invalid')
            {
                window.location.replace('../index.html');
            }
    		document.getElementById('error').innerHTML = `Error: ${data['error']}`;
    		document.getElementById('error').style.display = 'block';
    	}
    	else
    	{
    		document.getElementsByClassName('attendant-form')[0].innerHTML = `
    		<div class="success">
    			<h1>New Employee ${firstName} ${lastName}  has been added</h1>
    			<a href='new-attendant.html' class="btn-main">Add new employee</a>
    		</div>
    		`
    	}
    })
    .catch((error) => {console.log(error)})
}
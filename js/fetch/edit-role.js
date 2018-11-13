let params = (new URL(document.location)).searchParams;
let user = params.get("user");

window.addEventListener('load',userName)
function userName()
{
	url = `http://storemanage3000.herokuapp.com/api/v2/attendants/${user}`
	fetch(url,{
		"method": "GET",
		"mod": "cors",
		headers: {
		"Content-type": "application/json",
		"Access-Control-Allow-Origin":"*",
		"X-API-KEY": localStorage.getItem('token')
		}
	})
	.then((res) => {status = res.status; return res.json()})
	.then((data) => {
		document.getElementById('user-name').innerHTML = `Edit ${data['first name']} ${data['last name']}`;
	})
	.catch((error) => {console.log(error)})
}

document.getElementsByClassName('btn-main')[1].addEventListener('click',updateRole)

function updateRole()
{
	let role = document.getElementById('role').value;
	url = `http://0.0.0.0:5000/api/v2/attendants/${user}`;
	let payload = {"user type": role}
	fetch(url,{
		"method": "PUT",
		"mod": "cors",
		headers: {
		"Content-type": "application/json",
		"Access-Control-Allow-Origin":"*",
		"X-API-KEY": localStorage.getItem('token')
		},
		body: JSON.stringify(payload)
	})
	.then((res) => {status = res.status; return res.json()})
	.then((data) => {
		document.getElementById('role-result').innerHTML=data['message']
	})
}
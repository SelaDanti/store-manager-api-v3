let attendantsUrl = 'http://0.0.0.0:5000/api/v2/attendants';
let tableHead = `
	<table>
			<tr>
				<th colspan="9" id="product-title">Store Attendants details</th>
			</tr>
			<tr id="hover-body">
				<th>ID</th>
				<th>First Name</th>
				<th>Last Name</th>
				<th>Email</th>
				<th>Role</th>
				<th></th>
				<th></th>
			</tr>
`
window.addEventListener('load',getAttendants)

function getAttendants()
{
	fetch(attendantsUrl,{
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
		if (status != 200)
		{
			if (data['error'] == 'token is invalid')
			{
				window.location.replace('../index.html');
			}
			document.getElementById('attendants').innerHTML = `
			${tableHead}
			<tr>
				<td colspan="8" class="center">${data['error']}</td>
			</tr>
			
			
			
		</table>
			`
		}
		else
		{
			let body = ``
			for (x in data)
			{
				body += `
				<tr>
				<td>${data[x]['id']}</td>
				<td>${data[x]['first name']}</td>
				<td>${data[x]['last name']}</td>
				<td>${data[x]['email']}</td>
				<td>${data[x]['user type']}</td>
				<td>
				<a href="editrole.html?user=${data[x]['id']}" class="btn-edit">Edit role</a>
				</td>
				<td>
				<a href="sales-record.html?user=${data[x]['id']}" class="btn-category">view sales</a>
				</td>
				</tr>
				`
			}
			document.getElementById('attendants').innerHTML = `
			${tableHead} ${body}
			`
		}
	})
}
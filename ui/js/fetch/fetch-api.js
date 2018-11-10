function postData(url,data){	
	fetch(url,{
				"method": "POST",
				"mode":"cors",
				headers: {
			      "Content-type": "application/json",
			      "Access-Control-Allow-Origin":"*"
			    },
			    body: JSON.stringify(data)
	})
    .then((response) => {return response.json()})
    .then((data) => {
        console.log(data);
        })
        .catch((error) => {
        console.log(error);
    });
}

function putData(url,data){	
	fetch(url,{
				"method": "POST",
				"mode":"cors",
				headers: {
			      "Content-type": "application/json",
			      "Access-Control-Allow-Origin":"*"
			    },
			    body: JSON.stringify(data)
	})
    .then((response) => {return response.json()})
    .then((data) => {
        console.log(data);
        })
        .catch((error) => {
        console.log(error);
    });
}
postData('http://0.0.0.0:5000/api/v2/auth/login',{'email':'kwame','password'})
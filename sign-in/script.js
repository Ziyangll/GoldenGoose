function login(username,password)
{
	console.log("u: "+username)
	console.log("p: "+password)
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://127.0.0.1:8080/login/", true); // true for asynchronous 
    xmlHttp.send(JSON.stringify({"username":username,"password":password}));
    xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == XMLHttpRequest.DONE) {
			alert(xmlHttp.responseText);
		}
	}
}
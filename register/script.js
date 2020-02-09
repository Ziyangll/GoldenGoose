function createAccount(username,password)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://127.0.0.1:8080/create/", true); // true for asynchronous 
    xmlHttp.send(JSON.stringify({"username":username,"password":password}));
    xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == XMLHttpRequest.DONE) {
			alert(xmlHttp.responseText);
		}
	}
}
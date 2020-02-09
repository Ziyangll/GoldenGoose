function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("POST", theUrl, true); // true for asynchronous 
    xmlHttp.send(JSON.stringify({"username":"someone","password":"123456"}));
    xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == XMLHttpRequest.DONE) {
			alert(xmlHttp.responseText);
		}
	}
}

function writeyes() {
	console.log("yes");
}

httpGetAsync("http://127.0.0.1:8080/create/",writeyes)
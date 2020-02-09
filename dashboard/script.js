function load_table() {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("POST", "http://127.0.0.1:8080/owned/", true); // true for asynchronous 
	xmlHttp.send(JSON.stringify({"a":"a"}));
	let instr="";
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == XMLHttpRequest.DONE) {
			//alert(xmlHttp.responseText);
			inarr=xmlHttp.responseText.split("|");
			for(var i=0;i<25;i++) {
				document.getElementById("ta"+i.toString()).innerHTML = inarr[i];
			}
		}
	}
}
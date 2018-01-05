function getCurrentTabUrl(callback) {
	var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, (tabs) => {
  	var tab = tabs[0];
  	var url = tab.url;
  	console.assert(typeof url == 'string', 'tab.url should be a string');
    callback(url);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  getCurrentTabUrl((url) => {
  	var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
	    if(this.readyState == 4 && this.status == 200) {
	    	document.getElementById("message").style.display = 'none';
	        document.getElementById("amount").innerHTML = "Percentage of Clickbaitness is " + this.responseText + " %";
	    }
    }
        req.open('POST', 'http://127.0.0.1:5000/', true);
        req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        req.send("url=" + url);
  });
});
document.getElementById('youtube-url').value="https://www.youtube.com/watch?v=e2ZPKsTVSow";
document.getElementById("submit").click();

/*
Here, we wait.
*/

var children =  document.getElementById("dl_link").childNodes;
for(child in children)
{
	if (children.hasOwnProperty(child)){
		if(children[child].style.display=="")
		{
			children[child].click();
			break;
		}
} 		

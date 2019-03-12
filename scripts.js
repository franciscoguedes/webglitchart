
function openForm(){
	var form = document.getElementById("myForm");
	form.style.display = "flex";
}

function closeForm(){
	var form = document.getElementById("myForm");
	form.style.display = "none";
}

window.onclick = function(event){
	var form = document.getElementById("myForm");
	if (event.target == form){
		form.style.display ="none";
	}
}
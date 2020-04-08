

function slider_onchange(element){
	if (element.value) {
		element.parentElement.classList.add('forced')
	} else {
		element.parentElement.classList.remove('forced')
	}
}

function slider_onload(element){
	console.log(element);
	if (element.getAttribute("value") && element.parentElement.classList.contains('container')) {
		element.parentElement.classList.add('forced');
	}
}

document.addEventListener('DOMContentLoaded', function(){
	console.log("???");
Array.from(document.getElementsByTagName("input")).forEach(slider_onload)});
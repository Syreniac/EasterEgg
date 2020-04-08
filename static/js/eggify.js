const EGGIFY_COLOURS = ['#FFBDE8','#BDE8FF','#E8FFBD','#FFE8BD','#E8BDFF']

function eggify(element){
	console.log("Eggifying "+element);
	var seed = parseInt(element.dataset.seed);
	if(seed === undefined){
		seed = 0;
	}
	for(i = 0; i < 5; i++){
		var new_div = document.createElement("div");
		new_div.style.backgroundColor = EGGIFY_COLOURS[(i + seed) % EGGIFY_COLOURS.length];
		if(i != 0){
			new_div.style.borderTop = "2px solid #fff";
		}
		new_div.className = "stripe";
		element.appendChild(new_div);
	}
}

document.addEventListener('DOMContentLoaded', function(){
Array.from(document.getElementsByClassName("eggify")).forEach(eggify);
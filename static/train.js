document.getElementById('selectlayers').addEventListener("click", getlayers);
$("#layerform").submit(function(e) {
    e.preventDefault();
});

function getlayers(){
	var x = document.getElementById("#oflayers").value;
	var div = document.getElementById("layers");
	div.innerHTML = "";
	for (i=0; i<x; i++) {
		if (x > 5) {
			return;
		}
		var temp = document.createElement("input");
		temp.type = "number";
		temp.name = "hiddenlayers";
		temp.min = "0";
		temp.required = true;
		var label = document.createElement("label");
		label.innerHTML = 'Hidden layer ' + (i+1);
		div.appendChild(label);
		div.appendChild(temp);
	};
}

var slider = document.getElementById("data_slider");
var current = document.getElementById("currentrange");
current.innerHTML = slider.value;

slider.oninput = function(){
	current.innerHTML = this.value;
}

function hide(){
	var tohide = document.getElementsByClassName("onload");
	var toshow = document.getElementById("animation");
	for (i=0, len = tohide.length; i<len; i++){
		tohide[i].style.display = "none";
	}
	toshow.style.display ="block";
	toshow.style.background = "black";
	document.body.style.background = "black";
	
}

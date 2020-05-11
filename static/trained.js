var canvas = document.getElementById("draw");
var barh  = document.getElementById("bar").offsetHeight;
canvas.width = 300;
canvas.height = 300;
const context = canvas.getContext("2d");
context.lineWidth = 18;
var down = false;
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mousedown", function() {
	down = true;
	context.beginPath();
	context.moveTo(xpos, ypos);
	canvas.addEventListener("mousemove", draw)
});
canvas.addEventListener("mouseup", function() {down = false});
function draw(e) {
	xpos = (e.clientX - canvas.offsetLeft);
	ypos = (e.clientY - canvas.offsetTop);

	if(down == true){
		context.lineTo(xpos, ypos);
		context.stroke();
	}
}
function ge(){
	var imgdata = context.getImageData(0, 0, canvas.width, canvas.height);
	return imgdata.data;
}
function load(){
	document.getElementById("answer").innerHTML = "loading";
}
document.body,onkeyup = function(e){
	if(e.keyCode == 13){
		load();
		var imgd = ge();
		var i =3;
		var newd = [];
		for (; i<imgd.length;){
			newd.push(imgd[i]);
			i = i+4;
		}
		$.post("/givenumber", {"img":newd}, function(data){
			document.getElementById("answer").innerHTML = "PREDICTION " + data.number
		});
		
	}
}
document.body.onkeyup = function(e){
	if(e.keyCode == 32){
		context.clearRect(0, 0, canvas.width, canvas.height);
	}
}
var down = false;
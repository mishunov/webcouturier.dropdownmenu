function sfHover() {
	var sfEls = document.getElementById("portal-globalnav").getElementsByTagName("LI");
    // alert("DEBUG");
	for (var i=0; i<sfEls.length; i++) {
		sfEls[i].onmouseover=function() {
			this.className+=" sfhover";
		}
		sfEls[i].onmouseout=function() {
			this.className=this.className.replace(new RegExp(" sfhover\\b"), "");
		}
	}
}
if (window.attachEvent) {
    registerPloneFunction(sfHover);
}
'use strict';

$(function() {
	function setup() {
		demoFunction();
		sayHello();
	}

	function demoFunction() {
		//Write your amazing code here
	}

	function sayHello() {
		if (navigator.userAgent.toLowerCase().indexOf("chrome") > -1) {
			var t = ["\n %c Made with ♥ by Deuse %c https://www.deuse.be/ 👨‍💻 %c \n\n", "color: #fff; background: #F4C844; padding:5px 0;", "color: white; background: #1D1D1D; padding:5px 5px;","background:white;"];
			window.console.log.apply(console, t)
		} else {
			window.console && window.console.log("Made with love ♥ by Deuse - https://www.deuse.be/ 👨‍💻 ");
		}
	}

	setup();
});

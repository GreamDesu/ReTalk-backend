jQuery(document).ready(function($) {

	$('#menu').prepend('<h4><a href="#">Vis/skjul meny</a></h4>');
		$('#menu h4 a').click(function() {
		$('#menu ul').slideToggle();
		return false;
	});

	if ($('#theme').is(':hidden')) {
	
		// randomness
		var randomness = Math.round(Math.random() * 1);		

		if (randomness == 1) {
			$('#menu').addClass('v2');
		} else {
			$('#menu').addClass('v1');
		}
	
	}

});
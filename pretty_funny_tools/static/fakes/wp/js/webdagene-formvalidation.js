jQuery(document).ready(function($) {
	var registerForm = $('#register-form');

    if(registerForm.length) {
        registerForm.submit(function(event) {
            if($('#register-email').val() != $('#register-email-repeat').val()) {
                alert('E-mails doesn\'t match!');
                event.preventDefault();
            }
        });
    }
});
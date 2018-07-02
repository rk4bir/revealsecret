function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-]{3,152})+\@(([a-zA-Z0-9-]{2,10})+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}

function isUser(username) {
  var regex = /^([a-zA-Z0-9_])+$/;
  return regex.test(username);
}

function passwordStrength(password){
	var strength = 1;
	var arr = [/.{5,}/, /[a-z]+/, /[0-9]+/, /[A-Z]+/];
	jQuery.map(arr, function(regexp) {
	  if(password.match(regexp))
	     strength++;
	});
	
	if( strength == 1 ){
		return "Very weak";
	}else if( strength == 2 ){
		return "Weak";
	}else if( strength == 3 ){
		return "Medium";
	}else if( strength == 4 ){
		return "Strong";
	}else if( strength == 5 ){
		return "Very strong";
	}
}

var err = 0;

$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
	$( "#username" ).keyup(function() {
	  	var usr = $(this).val();
	  	if ( usr.length < 3 ){
	  		err += 1;
	  		$("#usrMessage").html('<i class="fa fa-close text-danger"> Too small</i>');
	  	}else if ( usr.length >= 3 ){
	  		$("#usrMessage").html('<i class="fa fa-check text-success"></i>');
	  		if ( usr.length > 32 ){
	  			err += 1;
		  		$("#usrMessage").html('<i class="fa fa-close text-danger"> Too large</i>');
		  	}else{
		  		if( !isUser(usr) ){
		  			err += 1;
			  		$("#usrMessage").html('<i class="fa fa-close text-danger"> Username contains invalid characters</i>');
			  	}else{
			  		$("#usrMessage").html('<i class="fa fa-check text-success"></i>');
			  	}
		  	}
	  	}	
	});

	$( "#email" ).keyup(function() {
	  	var email = $(this).val();
	  	if( !isEmail(email) ){
	  		err += 1;
	  		$("#emailMessage").html('<i class="fa fa-close text-danger"> Invalid email</i>');
	  	}else{
	  		$("#emailMessage").html('<i class="fa fa-check text-success"></i>');
	  	}

	});


	$( "#password" ).keyup(function() {
	  	var password = $(this).val();
	  	if( password.length < 6 ){
	  		err += 1;
	  		$("#passwordMessage").html('<i class="fa fa-close text-danger"> Too small password</i>');
	  	}else{
	  		$("#passwordMessage").html('<i class="fa fa-check text-success"> <b>Strength: </b>' + passwordStrength(password) + "</i>");
	  	}

	});


	$( "#re_password" ).keyup(function() {
	  	var re_password = $(this).val();
	  	var password = $("#password").val();
	  	if( re_password == password ){
	  		err += 1;
	  		$("#repasswordMessage").html('<i class="fa fa-check text-success"></i>');
	  	}else{
	  		$("#repasswordMessage").html("<i class='fa fa-close text-danger'> Password didn't match</i>");
	  	}
	});



	
	var showpass = false
	$("#show_pass").click(function(){
		var pval = $("#password").val()
		if( showpass == false ){
		    $("#password").replaceWith('<input class="form-control" id="password"  placeholder="Password" name="password" value="' + pval + '" type="text" required>');
			showpass = true;
		}else{
			$("#password").replaceWith('<input class="form-control" id="password"  placeholder="Password" name="password" value="' + pval + '" type="password" required>');			
			showpass = false;
		}
	});

	$("#message").keyup(function() {
	  	var msg = $(this).val();
	  	var remain = 260 - msg.length;
	  	if( remain < 1 ){
	  		$("#showRemain").html("<span class='text-danger'>Hint: You have remain " + remain + " character</span>");
	  	}else{
	  		$("#showRemain").html("<span class='text-primary'>Hint: You have remain " + remain + " characters</span>");
	  	}
	});

	
	
});
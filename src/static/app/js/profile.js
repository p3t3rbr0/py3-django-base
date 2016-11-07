var Profile = (function(){
	return {
		init: function() {
			this.el = {
				form: $('#profile-form'),
				username_input: $('input[name="username"]'),
				email_input: $('input[name="email"]'),
				avatar_input: $('input[name="avatar"]'),
				fname_input: $('input[name="fname"]'),
				lname_input: $('input[name="lname"]'),
				info_input: $('input[name="info"]'),
				errors: $('#errors-block'),
				ok_modal: $('.saved-ok-modal')
			};

			this.events();
		},

		events: function(){
			var self = this;
			
			/* Enable username field */
			$('#edit-username-btn').on('click',function(e){
				e.preventDefault();
				self.el.username_input.attr('disabled',false);
			});

			/* Enable email field */
			$('#edit-email-btn').on('click',function(e){
				e.preventDefault();
				self.email_input.attr('disabled',false);
			});

			/* Avatar upload preview */
			var avatar;
			self.el.avatar_input.on('change',function(e){
				var files = e.target.files;
				if(files && files[0]){
					var reader = new FileReader();
					reader.onload = function(e){
						$('#avatar').attr({
							src: e.target.result,
							width: 282
						});
					};
					avatar=files[0];
					reader.readAsDataURL(files[0]);
				}
			});

			/* Submit form */
			$('#submit').on('click',function(e){
				var fd = new FormData($('form').get(0));
				fd.append('username',self.el.username_input.val());
				fd.append('email',self.el.email_input.val());
				fd.append('avatar',self.el.avatar_input[0].files[0]);
				fd.append('info',self.el.info_input.val());
				fd.append('fname',self.el.fname_input.val());
				fd.append('lname',self.el.lname_input.val());

				_request({
					url: self.el.form.attr('action'),
					method: 'post',
					data: fd,
					params: {
						processData: false,
						contentType: false,
						csrf_token: '{{ csrf_token }}',
						csrf_name: 'csrfmiddlewaretoken',
						csrf_xname: 'X-CSRFToken'
					}
				}).then(function(resp){
					self.showOk();
				}).catch(function(err){
					self.showError({errors: {msg: 'Error'}});
				});
			});
		},

		showError: function(errors){
			var html = '<ul>';
			this.el.errors.html('');
			
			for(var err in errors)
				if(errors.hasOwnProperty(err)) html += '<li>'+errors[err]+'</li>';
			
			html += '</ul>';
			this.el.errors.html(html);
			this.el.errors.show();
		},

		showOk: function(){
			this.el.ok_modal.modal('show');
		}
	};
})();

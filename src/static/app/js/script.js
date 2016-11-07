var _request = function(opt){
	return new Promise(function(resolve,reject){
		if (!opt.url) reject(new TypeError("Url not found"));
		
		$.ajax({
			url: opt.url,
			type: opt.method ? opt.method : 'GET',
			cache: opt.cache ? opt.cache : false,
			contentType: false,
			processData: false,
			data: opt.data,
			params: opt.params || {}
		}).done(function(resp){
			resp = JSON.parse(resp);
			if(resp.error) reject(resp.error);
			resolve(resp);
		}).fail(function(err){reject(err);});
	});
};

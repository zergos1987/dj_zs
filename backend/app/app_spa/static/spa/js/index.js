"use strict";


let client_data = {"crb": 0};
let client_request;
let update_client_data = debounce(() => {send_ajax_post(app_url, client_data)}, client_data["crd"] || 500);


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};


function send_ajax_post(url, request_data) {
    return $.ajax({
        mode: 'same-origin',
        type: 'POST',
        dataType: 'JSON',
        //contentType: "application/json",
        contentType: false,
        processData: false,
            headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        data: request_data,
        url: url,
        success: function(server_data) {
            client_data = server_data;
            console.log("done", client_data);
        },
        error: function() {
            console.log("error");
        },
    });
}

if (client_data["crb"] == 0) {
    client_request = update_client_data();
}
console.log(client_request, 111111111)
//console.log(getCookie('csrftoken'));

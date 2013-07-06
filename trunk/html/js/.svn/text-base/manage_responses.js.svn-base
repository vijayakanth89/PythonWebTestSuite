
function main(app_id, configs) {

		var form = document.createElement('form');
		form.setAttribute("action","/");
		form.setAttribute("name","myform");
		form.setAttribute("id","myform");
		form.setAttribute("method","post");

		var hidden = document.createElement('input');
		hidden.setAttribute("name","app_id");
		hidden.setAttribute("value",app_id);
		hidden.setAttribute("type","hidden");
		form.appendChild(hidden);
	
		var requestCodes = "";		
		var obj = jQuery.parseJSON(configs);
		for (var key in obj) { 

			requestCodes += key + ":"
	
			var h = document.createElement('h');
			h.appendChild(document.createTextNode(key));
			form.appendChild(h);

			var select = document.createElement('select');
			select.setAttribute("id", key);
			select.setAttribute("name",key);
		
			var list = obj[key]
			for (var i = 0; i < list.length ; i++) {
				var option = document.createElement('option');
				option.setAttribute("value",list[i]);
				option.appendChild(document.createTextNode(list[i]));
				select.appendChild(option);
			}

			form.appendChild(select);
			form.appendChild(document.createElement("br"));
		}

		hidden = document.createElement('input');
		hidden.setAttribute("name","selected_keys");
		hidden.setAttribute("value",requestCodes);
		hidden.setAttribute("type","hidden");
		form.appendChild(hidden);

		var submit = document.createElement('input');
		submit.setAttribute("id","save");
		submit.setAttribute("value","save");
		submit.setAttribute("type","submit");
		form.appendChild(submit);
	
		document.getElementById('result').appendChild(form);

}

function handle_json(data) {
	var obj = jQuery.parseJSON(data);

	var form = document.getElementById('myform');
	var saveButton = document.getElementById('save');
	for (var key in obj) {

			var selectNode = document.getElementById(key);
			//removing the option child if any select Node
			if (selectNode != null) {
				while (selectNode.firstChild) {
					selectNode.removeChild(selectNode.firstChild);
				}
			} else {
                //create a new selection Node 
				selectNode = document.createElement('select');
				selectNode.setAttribute("id", key);
				selectNode.setAttribute("name",key);

				var h = document.createElement('h');
				h.appendChild(document.createTextNode(key));
				form.insertBefore(h,saveButton);
				form.insertBefore(selectNode,saveButton);
				form.insertBefore(document.createElement("br"),saveButton);
			}
			

			var list = obj[key]
			for (var i = 0; i < list.length ; i++) {
				var option = document.createElement('option');
				option.setAttribute("value",list[i]);
				option.appendChild(document.createTextNode(list[i]));
				selectNode.appendChild(option);
			}

	}
}

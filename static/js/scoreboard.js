
$(document).ready(function(){
	function sortTable() {
	  var table, rows, switching, i, x, y, shouldSwitch;
	  table = document.getElementById("scoreTable");
	  switching = true;
	  /* Make a loop that will continue until
	  no switching has been done: */
	  while (switching) {
		// Start by saying: no switching is done:
		switching = false;
		rows = table.rows;
		/* Loop through all table rows (except the
		first, which contains table headers): */
		for (i = 1; i < (rows.length - 1); i++) {
		  // Start by saying there should be no switching:
		  shouldSwitch = false;
		  /* Get the two elements you want to compare,
		  one from current row and one from the next: */
		  x = rows[i].getElementsByTagName("TD")[1];
		  y = rows[i + 1].getElementsByTagName("TD")[1];
		  // Check if the two rows should switch place:
		  if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
			// If so, mark as a switch and break the loop:
			shouldSwitch = true;
			break;
		  }
		}
		if (shouldSwitch) {
		  /* If a switch has been marked, make the switch
		  and mark that a switch has been done: */
		  rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
		  switching = true;
		}
	  }
	}
		console.log('connecting')
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    //receive message details from server
    socket.on('newmessage', function(msg) {
        console.log("Received message" + msg.message);
		var newSpan = document.createElement('span');
		newSpan.textContent = msg.message;
		newSpan.className = 'feedElement';
		var list = document.getElementById('feed');
		list.insertBefore(newSpan, list.childNodes[0]);
		
		if(list.childNodes.length > 5){
			list.removeChild(list.childNodes[5]);
		}
		
		var username = msg.message.split(' ')[0];
		console.log(username);
		
		var table = document.getElementById("scoreTable")
		var found = false;
		for (i = 1; i < (table.rows.length); i++) {
			var row = table.rows[i];
			console.log(row.getElementsByTagName('TD'));
			console.log(row.getElementsByTagName('TD')[0].innerHTML)
			if (row.getElementsByTagName('TD')[0].innerHTML === username) {
				row.getElementsByTagName('TD')[1].innerHTML = (parseInt(row.getElementsByTagName('TD')[1].innerHTML) + 1).toString();
				found = true;
				break;
			}
		}
		if(found){
			sortTable();
		}
		else{
			var tr = document.createElement('tr')
			var td1 = document.createElement('td')
			var td2 = document.createElement('td')
			
			td1.innerHTML = username;
			td2.innerHTML = '1';
			tr.appendChild(td1);
			tr.appendChild(td2);
			table.appendChild(tr);
		}
    });

});
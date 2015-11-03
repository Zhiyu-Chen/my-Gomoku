$(document).ready(function() {
	document.player_id = $('#player_id').val();

	setTimeout(requestPlay,0);


	$('#gomoku').click(function (event){
		var clickX = event.clientX + document.body.scrollLeft;
   		var clickY = event.clientY + document.body.scrollTop;
   		var center = getCenterXY(clickX,clickY);
		jQuery.ajax({
				url:'//localhost:8000/play',
				type:'Post',
				data:{
					player_id:document.player_id,
					x:center.x,
					y:center.y,
					action:'click',
				},
				dataType:'json'
			});
	});
});


//GET THE CENTER POSITION 
function getCenterXY(clickX, clickY) {
        var center = {};
        //-25原因是margin为25
        var modX = (clickX - marginInit) % gridLength, modY = (clickY - marginInit) % gridLength;
        if (modX < 25) {
            center.x = clickX - modX;
        } else {
            center.x = clickX - modX + 50;
        }
        if (modY < 25) {
            center.y = clickY - modY;
        } else {
            center.y = clickY - modY + 50;
        }
        return center;
    }


function requestPlay() {
	var host = 'ws://localhost:8000/play/status?playe_id=' + document.player_id;
	
	var websocket = new WebSocket(host);
	
	websocket.onopen = function (evt) {
		console.log('connected: ' + $('#player_id').val());
	};

	websocket.onmessage = function(evt) { 
		//console.log($.parseJSON(evt.data)['board']);
		//record = $.parseJSON(evt.data)['board']
		data = evt.data;
		data = data.replace(/'/g, "");
		record = JSON.parse(data);
		records = record[0];
		isOver = record[1];

		console.log(record[0]);
		console.log(record[1]);
		var board = document.getElementById("gomoku");
		var context = board.getContext("2d");
		context.beginPath();
        context.arc(records[0],records[1], radius, 0, 2 * Math.PI, false);
        context.stroke();
        context.closePath();
        if(records[2] == 1)
       		context.fillStyle = "#FFFFFF";
       	if(records[2] == 0)
       		context.fillStyle = "#000000";
        context.fill();
	};
	websocket.onerror = function (evt) { };
}
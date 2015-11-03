
	var boardWidth = 950,   
	    boardHeight = 950, 
	    marginInit = 25,    
	    gridLength = 50,    
	    row = 19,           
	    column = 19,       
	    radius = 20;       

	var board = document.getElementById("gomoku");
	var context = board.getContext("2d");
    context.clearRect(0, 0, boardWidth, boardHeight);
    //draw the margin
    context.strokeRect(0, 0, boardWidth, boardHeight);
    context.strokeStyle = "#000";
    //draw vertical lines
    context.beginPath();
    for (var i = 0; i < column; i++) {
        context.moveTo(marginInit + gridLength * i, 25);
        context.lineTo(marginInit + gridLength * i, 925);
    }
    //draw horizental lines
    for (var j = 0; j < row; j++) {
        context.moveTo(25, marginInit + gridLength * j);
        context.lineTo(925, marginInit + gridLength * j);
    }
    context.stroke();

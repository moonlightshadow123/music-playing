var VF = Vex.Flow;

function noteTrim(key){
	key = key.charAt(0).toUpperCase() + key.substring(1, key.length-2) + key.charAt(key.length-1);
	return key;
}

function display(cur_notes, id, clef){ //clef, note
	console.log(cur_notes);
	var area = document.getElementById(id);
	area.value = "";
	var count = 0;
	if(cur_notes.length == 0){
		area.value = " ";
		return;
	}
	cur_notes.forEach(function(e,i){
		if(e[0] == clef){
			area.value += (noteTrim(e[1]) + " \n ");
			count +=1;
		}
	});
	var pre_text = " ";
	if(count<7){
		var i = 0;
		for(i=0;i<(7-count)/2;i++){
			pre_text += "\n ";
		}
	}
	area.value = pre_text + area.value;
}
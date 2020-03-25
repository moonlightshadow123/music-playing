
function request(){
	  var list = [[["c#/4", "#", 4]], [["c/4","", 4]],[["d/4", "", 8]],[["d/4", "", 8]], [["c#/4","#", 4],["d/4","", 4,]]];
  var list2 =  [[["c#/3", "#", 4]], [["c/3","", 4]],[["d/3", "", 8]],[["d/3", "", 8]], [["c#/3","#", 4],["d/3","", 4,]]];
  var data = {"tre_notes_raw":list.concat(list), "bas_notes_raw":list2.concat(list2)}
  return data;
}

function draw_line(){
	var newLine = document.createElementNS('http://www.w3.org/2000/svg','line');
	newLine.setAttribute('id','line2');
	newLine.setAttribute('x1','50');
	newLine.setAttribute('y1','50');
	newLine.setAttribute('x2','50');
	newLine.setAttribute('y2','250');
	newLine.setAttribute("stroke", "blue");
	newLine.setAttribute("stroke-width", "2");
	(document.getElementsByTagName("svg")[0]).appendChild(newLine);

	line = SVG(newLine);
	return line;
}

function create_notes(notes_raw, clef){
    var notes = [];
    notes_raw.forEach(function(tick_note,index){
      var keys = tick_note.map(function(e, i){return e[0]});
      var accs = tick_note.map(function(e, i){return e[1]});
      var durs = tick_note.map(function(e, i){return e[2]});
      var note = new VF.StaveNote({
        clef: clef,
        keys: keys,
        duration: durs[0].toString(),
      });
      accs.forEach(function(e,i){
        if(e) note.addAccidental(i, new VF.Accidental(e));
      });
      notes.push(note);
      console.log(note);
    });
    return notes;
  }

function draw(data){

    // Create an SVG renderer and attach it to the DIV element named "boo".
    var div = document.getElementById("boo")
    var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

    // Configure the rendering context.
    renderer.resize(1000, 300);
    var context = renderer.getContext();
    context.setFont("Arial", 10, "").setBackgroundFillStyle("#eed");

    // Create a stave of width 400 at position 10, 40 on the canvas.
    var tre_stave = new VF.Stave(10, 40, 800);
    // Add a clef and time signature.
    tre_stave.addClef("treble").addTimeSignature("4/4");



    var bas_stave = new VF.Stave(10, 140, 800);
    bas_stave.addClef("bass").addTimeSignature("4/4");


    // Connect it to the rendering context and draw!
    tre_stave.setContext(context).draw();
    bas_stave.setContext(context).draw();

    //this.formatter = new VF.Formatter();

    var tickQue = []; // (svg_notes[], notes[], toshift)

   	var m_beats = 8;
    var m_value = 4;
    var measure_len = 800;
    var speed = 400/3000;
   

    var tre_notes_raw = data["tre_notes_raw"];
    var bas_notes_raw = data["bas_notes_raw"];
    var tre_notes = create_notes(tre_notes_raw, "treble");
    var bas_notes = create_notes(bas_notes_raw, "bass");

    var tre_voice = (new VF.Voice({num_beats: m_beats,  beat_value: m_value})).addTickables(tre_notes);
    var bas_voice = (new VF.Voice({num_beats: m_beats,  beat_value: m_value})).addTickables(bas_notes);

    console.log("There!");

    var formatter = new VF.Formatter().joinVoices([tre_voice, bas_voice]).format([tre_voice, bas_voice], measure_len);

    // Draw voices
    tre_voice.draw(context, tre_stave);
    bas_voice.draw(context, bas_stave);
    /*
    var group = this.context.openGroup();
    this.context.closeGroup();

    // Add group to groupQue
    var g_svg = SVG(group);
    g_svg.x(g_svg.x() + this.start_pos);
    this.groupQue.push([g_svg, this.start_pos+this.measure_len]); // (svg, to_shift)
    */
    console.log("Here!");

    // Add notes to tickQue
    var tick_list = formatter.tickContexts.array;
    var i = 0;
    var xs = tick_list.map(function(e, i){
    	var notes = e.tickables;
    	var shift = Math.min.apply(null, notes.map(function(e,i){return SVG(e.getAttribute("el")).x()}));
    	var strs = [];
    	notes.forEach(function(e, i){
    		var i = 0;
    		for(i=0;i<e.keys.length;i++){
    			strs.push([e.clef, e.keys[i]]);
    		}
    	});
    	return [shift, strs]
    });

  	return xs;
}

function move(line, tickQue){
	if(tickQue.length == 0) location.reload();
	console.log(tickQue);
	var cur_x = tickQue[0][0];
	var cur_notes = tickQue[0][1];
	display(cur_notes, "tre_area", "treble");
	display(cur_notes, "bas_area", "bass");
	console.log(cur_notes);
	var speed = 400/3000;
	var pre_x = line.x();
	//var cur_x = cur_note.x();
	line.animate({duration:(cur_x-pre_x)/speed}).x(cur_x);
	tickQue.shift();
}

function resize(){

}

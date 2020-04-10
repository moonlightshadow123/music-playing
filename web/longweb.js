var context;
var tre_stave;
var bas_stave;
var timeSign = "4/4";
var keySign = "C";

var line;
var xs = []; // (shift, nstrs)

var measure_len = 800;
var speed = 100;

function set_move_speed(s){
    speed = s;
    console.error("speed = "+ s.toString());
}

function set_m_k(m, k){
    timeSign = m;
    keySign = k;
    m_beats = parseInt(m.charAt(0))*2;
    m_value = parseInt(m.charAt(2));
}

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
    move();
}

function create_notes(notes_raw, clef){
    var notes = [];
    notes_raw.forEach(function(tick_note,index){
      if(tick_note == "|"){
        notes.push(new VF.BarNote()); return;
      }  
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

function draw_stave(){
    if(document.getElementsByTagName("svg").length > 0)
        document.getElementsByTagName("svg")[0].remove();
    var div = document.getElementById("boo")
    var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

    // Configure the rendering context.
    renderer.resize(1000, 300);
    context = renderer.getContext();
    context.setFont("Arial", 10, "").setBackgroundFillStyle("#eed");

    // Create a stave of width 400 at position 10, 40 on the canvas.
    tre_stave = new VF.Stave(10, 40, 900);
    // Add a clef and time signature.
    tre_stave.addClef("treble").addTimeSignature(timeSign);
    tre_stave.addModifier(new Vex.Flow.KeySignature(keySign));


    bas_stave = new VF.Stave(10, 140, 900);
    bas_stave.addClef("bass").addTimeSignature(timeSign);
    bas_stave.addModifier(new Vex.Flow.KeySignature(keySign));


    // Connect it to the rendering context and draw!
    tre_stave.setContext(context).draw();
    bas_stave.setContext(context).draw();

    document.getElementsByTagName("svg")[0].style.display = "inline";
    document.getElementsByTagName("svg")[0].style.float = "left";
}

/*
function draw_notes1(){

var musicObjects = [

new Vex.Flow.Barline("repeat_begin"),

new Vex.Flow.Clef("treble"),

new Vex.Flow.KeySignature("C#"),

new Vex.Flow.TimeSignature("4/4"),

new Vex.Flow.StaveNote({ keys: ["c#/4"], duration: "q" }),
new Vex.Flow.StaveNote({ keys: ["d/4"], duration: "q" }),
new Vex.Flow.StaveNote({ keys: ["b/4"], duration: "qr" }),
new Vex.Flow.StaveNote({ keys: ["c/4", "e/4", "g/4"], duration: "q" }),

new Vex.Flow.Barline("repeat_end")
];

Vex.Flow.Formatter.FormatAndDraw(context, tre_stave, musicObjects);
}
*/
function draw_notes(data){

    //this.formatter = new VF.Formatter();

    var tre_notes_raw = data["tre_notes_raw"];
    var bas_notes_raw = data["bas_notes_raw"];
    var tre_notes = create_notes(tre_notes_raw, "treble");
    var bas_notes = create_notes(bas_notes_raw, "bass");

    // VF.Beam({ notes: tre_notes });
    // VF.Beam({ notes: bas_notes });

    //var tre_voice = (new VF.Voice({num_beats: m_beats,  beat_value: m_value})).addTickables(tre_notes);
    //var bas_voice = (new VF.Voice({num_beats: m_beats,  beat_value: m_value})).addTickables(bas_notes);
    var tre_voice = (new VF.Voice()).setStrict(false).addTickables(tre_notes);
    var bas_voice = (new VF.Voice()).setStrict(false).addTickables(bas_notes);

    var tre_beams = VF.Beam.applyAndGetBeams(tre_voice);
    var bas_beams = VF.Beam.applyAndGetBeams(bas_voice, -1);

    console.log("There!");

    var formatter = new VF.Formatter().joinVoices([tre_voice, bas_voice]).format([tre_voice, bas_voice], measure_len);

    /*
    var tre_beams = VF.Beam.generateBeams(tre_notes);

    tre_beams.forEach(function(beam) {
        beam.setContext(context).draw();
    });    */



    // Draw voices
    tre_voice.draw(context, tre_stave);
    bas_voice.draw(context, bas_stave);

    tre_beams.forEach(function(beam) {
        beam.setContext(context).draw();
      });
    bas_beams.forEach(function(beam) {
        beam.setContext(context).draw();
      });
    /*
    var group = this.context.openGroup();
    this.context.closeGroup();

    // Add group to groupQue
    var g_svg = SVG(group);
    g_svg.x(g_svg.x() + this.start_pos);
    this.groupQue.push([g_svg, this.start_pos+this.measure_len]); // (svg, to_shift)
    */
    


    // Add notes to xs
    var tick_list = formatter.tickContexts.array;
    var i = 0;
    console.log(tick_list);
    // console.error(tick_list);
    tick_list.forEach(function(e, i){
    	var notes = e.tickables;
        try{ 
    	    var shift = Math.min.apply(null, notes.map(function(e,i){
                if(e.isRest()) return Infinity;
                return SVG(e.getAttribute("el")).x();
            }));
        }catch(error){ // For bar note
            return;
        }
        if(shift == Infinity) return; // For rest note 
    	// console.error(shift);
        var strs = [];
    	notes.forEach(function(e, i){
    		var i = 0;
    		for(i=0;i<e.keys.length;i++){
    			strs.push([e.clef, e.keys[i]]);
    		}
    	});
    	xs.push([shift, strs])
    });
    console.error("Xs!!!!!!!!!!!!!");
    console.error(xs.length);
    xs.sort(function(a, b){return a[0] - b[0];});
    xs.forEach(function(e, i){
        console.error(e);
    });
  	// return xs;
}

function move(){
    console.error(speed);
	if(xs.length == 0) return;
	var cur_x = xs[0][0];
	var cur_notes = xs[0][1];
	display(cur_notes, "tre_area", "treble");
	display(cur_notes, "bas_area", "bass");
	console.log(cur_notes);
	var pre_x = line.x();
	//var cur_x = cur_note.x();
	line.animate({duration:(cur_x-pre_x)/speed}).x(cur_x);
	xs.shift();
}

function resize(){

}

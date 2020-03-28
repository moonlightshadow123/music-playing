
var context;
var tre_stave;
var bas_stave;
var notes_dict = {};

function draw_stave(){
  var div = document.getElementById("boo")
  var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

  // Configure the rendering context.
  renderer.resize(150, 300);
  context = renderer.getContext();
  context.setFont("Arial", 10, "").setBackgroundFillStyle("#eed");

  // Create a stave of width 400 at position 10, 40 on the canvas.
  tre_stave = new VF.Stave(10, 40, 100);
  // Add a clef and time signature.
  tre_stave.addClef("treble");



  bas_stave = new VF.Stave(10, 140, 100);
  bas_stave.addClef("bass");


  // Connect it to the rendering context and draw!
  tre_stave.setContext(context).draw();
  bas_stave.setContext(context).draw();

}

function draw_note(data){

  var btnNum = data["btnIdx"]
  var key = data["noteStr"];
  var acc = data["acc"]
  var duration = "4";
  var clef = data["clef"];
  if(notes_dict[btnNum])
  return;

  var note = new VF.StaveNote({clef: clef, keys:[key], duration: duration});
  if(acc) note.addAccidental(0, new VF.Accidental(acc));

  // Create a voice in 4/4 and add above notes
  var voice = new VF.Voice({num_beats: 1,  beat_value: 4});
  voice.addTickables([note]);


  // Format and justify the notes to 400 pixels.
  var formatter = new VF.Formatter().joinVoices([voice]).format([voice], 400);

  // Render voice
  voice.draw(context, clef=="treble"?tre_stave:bas_stave);
  notes_dict[btnNum] = [clef, key, voice];
  
  var cur_notes = [];
    for(var btnNum in notes_dict){
      cur_notes.push(notes_dict[btnNum])
    }
  display(cur_notes, "tre_area", "treble");
  display(cur_notes, "bas_area", "bass");
}

function erase_note(btnNum){
  if(notes_dict.hasOwnProperty(btnNum)){
    var voice = notes_dict[btnNum][2];
    voice.tickables[0].attrs.el.remove();
    delete this.notes_dict[btnNum];
  }
  var cur_notes = [];
    for(var btnNum in notes_dict){
      cur_notes.push(notes_dict[btnNum])
    }
  display(cur_notes, "tre_area", "treble");
  display(cur_notes, "bas_area", "bass");

}



function reset(){

}

/*

class Staff{
  constructor(clef){
  // Create an SVG renderer and attach it to the DIV element named "boo".
  
  }
  drawNote(data){
var btnNum = data["btnNum"]
var note = data["note"];
var duration = data["duration"];
if(this.notes_dict[btnNum])
  return;

  var notes = [
    // A quarter-note C.
    new VF.StaveNote({clef: this.clef, btnNums:note, duration: duration}),
    ];

  // Create a voice in 4/4 and add above notes
  var voice = new VF.Voice({num_beats: 1,  beat_value: 4});
  voice.addTickables(notes);


  // Format and justify the notes to 400 pixels.
  var formatter = new VF.Formatter().joinVoices([voice]).format([voice], 400);

  // Render voice
  voice.draw(this.context, this.stave);
  this.notes_dict[btnNum] = voice;
  console.error(this.notes_dict);
}
eraseNote(btnNum){
  var voice;
  console.error(voice);
  voice = this.notes_dict[btnNum];
  if(voice!=undefined)
    voice.tickables[0].attrs.el.remove();
  delete this.notes_dict[btnNum];
}  
}
*/
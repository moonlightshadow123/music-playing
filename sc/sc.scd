(
s.boot;
NetAddr.langPort.postln;
~keys = Array.newClear(128);

SynthDef.new( \piano, { arg freq = 440, decay = 0.8, gate=1;
    var env, sig;
    env = EnvGen.kr( Env.asr(), gate, doneAction: 0 );
    sig = MdaPiano.ar(freq:freq,decay:decay);
    //sig = LFTri.ar( [ freq, freq * 0.999 ], 0.0, amp ) * env;
    //Out.ar( [ 0 ], sig * 0.6 );
    sig = sig * env;
    Out.ar(0, sig);
    //sig.play();
}).add;

OSCdef.new(
	\noteOn,
	{
		arg msg, time, addr, port;
		[msg, time, addr, port].postln;
		if(~keys[msg[1].asInteger].notNil){
			~keys[msg[1].asInteger].free
		};
		~keys[msg[1].asInteger] = Synth(\piano, [\freq, msg[2].asFloat]);
	},
	'/noteOn'
);

OSCdef.new(
	\clear,
	{
		arg msg, time, addr, port;
		s.freeAll;
	},
	'/clear'
);

OSCFunc({ | msg, time, addr, port |
	var x;
	[msg, time, addr, port].postln;
	msg[1].postln;
	~keys[msg[1].asInteger].set(\gate, 0);

	//x = {MdaPiano.ar(freq:msg[1].asInteger,decay:0.2)}.play();
},'/noteOff');
)

(
var timeNow;
TempoClock.default.tempo = 2;
timeNow = TempoBusClock.default.beats;
"Time is now: ".post; timeNow.postln;
TempoBusClock.default.schedAbs(timeNow + 5,
	{"Time is later: ".post; thisThread.clock.beats.postln; nil});
)
s.freeAll;

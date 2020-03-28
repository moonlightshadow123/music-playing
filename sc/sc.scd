(
s.boot;
NetAddr.langPort.postln;

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

~keys = Array.newClear(128);

/*
OSCFunc({ | msg, time, addr, port |
    var x;
    [msg, time, addr, port].postln;
    msg[1].postln;
    ~keys[msg[1].asInteger] = Synth.new(\piano, [\freq, msg[2].asInteger]);
    //x = {MdaPiano.ar(freq:msg[1].asInteger,decay:0.2)}.play();
},'/noteOn');
*/
OSCdef.new(
	\noteOn,
	{
		arg msg, time, addr, port;
		[msg, time, addr, port].postln;
		if(~keys[msg[1].asInteger]){
			~keys[msg[1].asInteger].set(/gate, 0);
		}
		~keys[msg[1].asInteger] = Synth.new(\piano, [\freq, msg[2].asFloat]);
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

s.freeAll;

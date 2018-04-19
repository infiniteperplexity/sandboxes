//@flow

let Monster = {template: "Monster"};

function createChild(obj) {
	let nobj = Object.create(obj);
	nobj.name = "";
	return (nobj: typeof nobj);
}

let Goblin = createChild(Monster);

let s: string = Goblin.template;
let n: number = Goblin.template;
let t: string = Goblin.thing;

Goblin.name = "Gob";
Goblin.height = 4;

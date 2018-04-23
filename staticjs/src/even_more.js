//@flow

let parent = {
	foo: 1,
	bar: function(b: number): number {
		let child = Object.create(this);
		child = Object.assign(child, args);
		return (child: {...typeof parent, ...T});
	}
};
parent.bar("foo");
type Recast = {...typeof parent, bar: (b: number | string)=> number | string};
parent = (parent: any);
parent = (parent: Recast);

parent.bar("foo");
parent.bar(false);
parent.foo = 5;

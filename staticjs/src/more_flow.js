//@flow
let foo = {a: 1, b: 2};
foo.c = 3;




let parent = {
	foo: 1,
	extend: function<T: Object>(args: T): {...typeof parent, ...T} {
		let child = Object.create(this);
		child = Object.assign(child, args);
		return (child: {...typeof parent, ...T});
	}
};
let child = parent.extend({
	bar: 2
});
child.bar;
child.baz;
let grandkid = child.extend({
	baz: 3
});
grandkid.bar;
grandkid.baz;
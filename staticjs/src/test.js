//@flow
let parent = {
	foo: 1,
	extend: function<T: Object>(args: T): {...typeof parent, ...T} {
		let child = Object.create(this, args);
		return (child: {...typeof parent, ...T});
	}
};
let child = parent.extend({
	bar: 2
});
child.bar;
// desired error
child.baz;
let grandkid = child.extend({
	baz: 3
});
grandkid.baz;
// undesired error
grandkid.bar;

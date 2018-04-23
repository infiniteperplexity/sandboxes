//@flow
let parent = {
	foo: 1,
	extend: function<T: Object>(args: T): {...typeof parent, ...T} {
		let child = Object.create(this);
		child = Object.assign(child, args);
		return (child: {...typeof parent, ...T});
	}
};
type Child = {...typeof parent, bar: number, extend: <T: Object>(args: T) => {...typeof child, ...T}};
let child = parent.extend({
	bar: 2
});
child = ((child: any): {...typeof parent, bar: number, extend: <T: Object>(args: T) => {...typeof child, ...T}});
// should not error
child.bar;
// should error
child.baz;
let grandkid = child.extend({
	baz: 3
});
// should not error
grandkid.bar;
grandkid.baz;
let ggrand = grandkid.extend({
	qux: 4
});

ggrand.qux;
ggrand.bar;
ggrand.baz;

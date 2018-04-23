//@flow
type AnyObject = {[key: string]: mixed
function extend<A: AnyObject, B: AnyObject>(a: A, b: B): {...A, ...B} {
	 let child = Object.create(a);
	 child = Object.assign(a, b);
	 return (child: {...A, ...B});
}

let parent = {
	foo: 1,
	// I actually want the return type to be based on "this", not "parent"
	extend: function<T: AnyObject>(args: T): * {
		return (extend(this, args): {...typeof this, ...T});
	}
};
let child = parent.extend({
	bar: 2
});
child.bar;
// I want this error...
child.baz;
let grandkid = child.extend({
	baz: 3
});
// ...but not this one:
grandkid.bar;
grandkid.baz;

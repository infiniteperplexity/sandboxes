//@flow

type Parent = {template: "Parent"};
type Args = {template: string};

let parent = {
  template: "Parent",
  foo: 1,
  extend: function<S: string, T: {template: S}>(template: S, args: T): {template: S} {
    let child: {template: S} = Object.create(this);
    child = Object.assign(child, args);
    return child;
  }
}




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

/* @flow */
type AnyObject = {[key: string]: mixed};

function extend<A: AnyObject, B: AnyObject>(a: A, b: B): {...A, ...B} {
  let child = Object.create(a);
  child = Object.assign(a, b);
  return (child: {...A, ...B});
}

let parent = {foo: 1};
let args: {bar: mixed} = {bar: 2};
let child = extend(parent, args);
child.bar;
child.baz;
let args2: {baz: mixed} = {baz: 3};
let grandkid = extend(child, args2);
grandkid.bar;
grandkid.baz;
grandkid.qux;

// cd C:\Users\Glenn Wright\Documents\GtHub\sandboxes\staticjs
// npm run flow type-at-pos src\flow.js 2 5

// couldn't figure out how to extract the actual type of a function
// the + symbol makes properties immutable, I think
// there's a gotcha with union types of objects, where you might need to make them exact
// $Shape, $Pred, and $Ref are secret types
// & and $Diff can I think be used to assemble and disassemble object types


/*

So...I'm running into this issue where I want to specify that an object...
...must have values of a certain type, if it has any values for certain keys...
...can take on additional keys in the future.

The latter part is the hard part.  I think it's basically just not allowed and you have to spread it.

Okay...I *think* I understand all this.

*/

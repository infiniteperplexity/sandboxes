//@flow
import type {Parent} from './src/chris.js';

let parent: Parent = {
  foo: 1,
  extend(args) {
    return {...this, ...args};
  }
};

let child = parent.extend({bar: 2});
child.foo;
child.bar;
child.baz;

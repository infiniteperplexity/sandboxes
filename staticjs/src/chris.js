//@flow
let parent = {
  foo: 1,
  extend(args: Object) {
    return {...this, ...args};
  }
};

export type Parent = typeof parent;

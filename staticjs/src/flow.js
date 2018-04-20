// @flow
Object.create;
//(o: any, properties?: PropertyDescriptorMap) => any

let f = function() {
	type fType = {foo: number} & {bar: string}; 
};

f();
//type fType = {foo: number} & {bar: string}; 

let baz: fType = {foo: 2, bar: "zap"};
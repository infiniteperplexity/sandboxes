//@flow
import type {Parent} from "./flow_one";
export type Child = Parent & {bar: "baz"};
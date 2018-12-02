import Vuex from "vuex";

export default function create(initial) {
    return new Vuex.Store({
        state: {
            ...{trans: {}},
            ...initial,
        },
        strict: false,
    });
}
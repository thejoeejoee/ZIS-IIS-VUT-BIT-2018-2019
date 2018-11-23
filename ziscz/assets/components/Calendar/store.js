import Vuex from "vuex";

export default function create(initial) {
    return new Vuex.Store({
        state: {
            ...{
                editable: false,
            },
            ...initial,
        },
        strict: false,
    });
}
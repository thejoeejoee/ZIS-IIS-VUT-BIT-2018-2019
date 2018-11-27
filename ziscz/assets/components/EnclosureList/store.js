import Vuex from "vuex";
import axios from "axios";
import reverse from 'django-reverse'
import _ from 'lodash'
import Toastr from 'toastr'


const saveAnimals = _.debounce((state, undo) => {
    axios.post(reverse('api:enclosure_animals_setup'), {
        enclosures: _.map(
            state.enclosures,
            (enc) => ({
                id: enc.id,
                animals: _.map(enc.animals, _.property('id'))
            })
        )
    }).then((resp) => {
        if (resp.data.success) {
            Toastr.success(resp.data.msg);
        } else {
            Toastr.warning(resp.data.msg);
            undo();
        }
    }, () => {
        undo();
    })
}, 200);

export default function create(initial) {
    return new Vuex.Store({
        state: {
            ...{
                enclosures: [],
                can_change_animal: false,
            },
            ...initial,
        },
        mutations: {
            setAnimals(state, {enclosure, animals}) {
                enclosure.animals = animals;
            },
            emptyState(state) {
                this.replaceState({
                    ...{
                        enclosures: [],
                        can_change_animal: false,
                    },
                    ...initial,
                });
            }
        },
        actions: {
            updateAnimals({commit, state}, {enclosure, animals, undo}) {
                commit('setAnimals', {enclosure, animals});
                saveAnimals(state, undo);
            }
        }
    });
}
import Vuex from "vuex";
import axios from "axios";
import reverse from 'django-reverse'
import _ from 'lodash'
import Toastr from 'toastr'


const saveAnimals = _.debounce((state) => {
    axios.post(reverse('api:enclosure_animals_setup'), {
        enclosures: _.map(
            state.enclosures,
            (enc) => ({
                id: enc.id,
                animals: _.map(enc.animals, _.property('id'))
            })
        )
    }).then(({data}) => {
        if (data.success) {
            Toastr.success(data.msg);
        } else {
            Toastr.warning(data.msg);
        }
    })
}, 200);

export default function create(initial) {
    return new Vuex.Store({
        state: {
            ...{
                enclosures: [],
            },
            ...initial,
        },
        mutations: {
            setAnimals(state, {enclosure, animals}) {
                enclosure.animals = animals;
            }
        },
        actions: {
            updateAnimals({commit, state}, {enclosure, animals}) {
                commit('setAnimals', {enclosure, animals});
                saveAnimals(state);
            }
        }
    });
}
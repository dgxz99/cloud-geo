// src/composables/useNavBar.js
import { useRouter } from 'vue-router';

export function useNavBar() {
    const router = useRouter();

    function navigate(route) {
        router.push(route);
    }

    return { navigate };
}

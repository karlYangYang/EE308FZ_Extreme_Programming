import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
    const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

    function setUser(newUser) {
        user.value = newUser
        localStorage.setItem('user', JSON.stringify(newUser))
    }

    function logout() {
        user.value = {}
        localStorage.removeItem('user')
    }

    function isLoggedIn() {
        return user.value && user.value.id
    }

    return { user, setUser, logout, isLoggedIn }
})

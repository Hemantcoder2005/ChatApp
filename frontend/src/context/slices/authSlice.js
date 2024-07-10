import axios from "axios";

export const createAuthSlice = (set) => ({
    user: JSON.parse(localStorage.getItem('chat-client')) || false,

    login: (userData) => {
        localStorage.setItem('chat-client', JSON.stringify(userData));
        set({ user: userData });
    },

    logout: () => {
        localStorage.removeItem('chat-client');
        set({ user: false });
      },

      validateToken: async () => {
        const user = JSON.parse(localStorage.getItem('chat-client'));
         if (user && user.accessToken){
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/accounts/")

                if (!response.data.error) {
                    set({ user });
                }else {
                    localStorage.removeItem('chat-client');
                    console.log(response.data)
                    set({ user: null });
                  }
            } catch (error) {
                console.error('Error validating token:', error);
            localStorage.removeItem('chat-client');
            set({ user: null });
            }
         }
      }
})
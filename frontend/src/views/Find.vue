<template>
    <div class="find-container">
        <h1>Trova Utenti</h1>

        <!-- Barra di ricerca -->
        <div class="search-box">
            <input ref="searchInput" type="text" v-model="searchQuery" @input="onSearchInput"
                placeholder="Cerca utenti..." class="search-input" :disabled="searching" autocomplete="off"
                autocapitalize="off" spellcheck="false">
            <div v-if="searching" class="loading">Caricamento...</div>
        </div>

        <!-- Risultati -->
        <div class="results">
            <!-- Nessun risultato -->
            <div v-if="searchQuery.length >= 2 && users.length === 0 && !searching" class="no-results">
                Nessun utente trovato per "{{ searchQuery }}"
            </div>

            <!-- Lista utenti -->
            <div v-if="users.length > 0" class="users-list">
                <p class="results-count">{{ total }} utenti trovati</p>

                <div v-for="user in users" :key="user.id" class="user-item">
                    <div class="user-info">
                        <div class="user-avatar">{{ user.username.charAt(0).toUpperCase() }}</div>
                        <div>
                            <div class="username">{{ user.username }}</div>
                            <div class="user-email" v-if="user.email">{{ user.email }}</div>
                        </div>
                    </div>

                </div>
            </div>

            <!-- Messaggio iniziale -->
            <div v-if="searchQuery.length === 0" class="initial-message">
                Inserisci almeno 2 caratteri per cercare utenti
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../utils/api.js'

export default {
    name: 'Find',
    setup() {
        const searchQuery = ref('')
        const users = ref([])
        const searching = ref(false)
        const total = ref(0)
        const lastSearchQuery = ref('')
        const searchInput = ref(null)
        let searchTimeout = null

        // Debounced search function
        const performSearch = async (query) => {
            if (query.length < 2) {
                users.value = []
                total.value = 0
                return
            }

            try {
                searching.value = true
                const response = await api.get('/api/users/find', {
                    params: { q: query, limit: 20 }
                })

                users.value = response.data.users || []
                total.value = response.data.total || 0
                lastSearchQuery.value = query

                // Mantieni il focus sull'input dopo aver ricevuto i risultati
                setTimeout(() => {
                    if (searchInput.value) {
                        searchInput.value.focus()
                    }
                }, 0)

            } catch (error) {
                console.error('Errore nella ricerca utenti:', error)
                users.value = []
                total.value = 0

                if (error.response?.status === 401) {
                    // Sessione scaduta, redirect al login
                    logout()
                    router.push('/login')
                }
            } finally {
                searching.value = false
            }
        }

        // Debounced input handler
        const onSearchInput = () => {
            clearTimeout(searchTimeout)
            searchTimeout = setTimeout(() => {
                performSearch(searchQuery.value.trim())
            }, 300) // 300ms delay
        }



        // Format date helper
        const formatDate = (dateString) => {
            try {
                const date = new Date(dateString)
                return date.toLocaleDateString('it-IT', {
                    year: 'numeric',
                    month: 'long'
                })
            } catch {
                return 'Data non disponibile'
            }
        }

        // Focus sull'input quando il componente viene montato
        onMounted(() => {
            if (searchInput.value) {
                searchInput.value.focus()
            }
        })

        return {
            searchQuery,
            users,
            searching,
            total,
            lastSearchQuery,
            searchInput,
            onSearchInput,
        }
    }
}
</script>

<style scoped>
/* Layout principale */
.find-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem 1rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    min-height: 100vh;
}

/* Titolo */
h1 {
    text-align: center;
    margin-bottom: 2rem;
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.025em;
}

/* Sezione ricerca */
.search-box {
    margin-bottom: 2rem;
}

.search-input {
    width: 100%;
    padding: 1rem 1.5rem;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    font-size: 1.1rem;
    background: white;
    transition: all 0.2s ease;
    box-sizing: border-box;
}

.search-input:focus {
    outline: none;
    border-color: #3182ce;
    box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1);
}

.search-input:disabled {
    background: #f7fafc;
    opacity: 0.6;
    cursor: not-allowed;
}

.loading {
    text-align: center;
    padding: 1rem;
    color: #718096;
    font-style: italic;
}

/* Area risultati */
.results {
    min-height: 300px;
}

.results-count {
    margin-bottom: 1.5rem;
    color: #4a5568;
    font-size: 0.95rem;
    font-weight: 500;
}

.no-results {
    text-align: center;
    padding: 3rem 2rem;
    color: #718096;
    background: white;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

.initial-message {
    text-align: center;
    padding: 4rem 2rem;
    color: #a0aec0;
    font-style: italic;
    background: white;
    border-radius: 12px;
    border: 1px dashed #e2e8f0;
}

/* Lista utenti */
.users-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.user-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    transition: all 0.2s ease;
}

.user-item:hover {
    border-color: #cbd5e0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    transform: translateY(-1px);
}

.user-info {
    background: white;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.user-avatar {
    width: 45px;
    height: 45px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1.1rem;
    flex-shrink: 0;
}

.username {
    font-weight: 600;
    color: #2d3748;
    font-size: 1.1rem;
    margin-bottom: 0.25rem;
}

.user-email {
    font-size: 0.9rem;
    color: #718096;
}

.add-btn {
    padding: 0.6rem 1.5rem;
    background: #3182ce;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.9rem;
}

.add-btn:hover:not(:disabled) {
    background: #2c5aa0;
    transform: translateY(-1px);
}

.add-btn:disabled {
    background: #a0aec0;
    cursor: not-allowed;
    transform: none;
}

/* Responsive */
@media (max-width: 768px) {
    .find-container {
        padding: 1.5rem 1rem;
    }
    
    h1 {
        font-size: 2rem;
    }
    
    .user-item {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
        padding: 1.25rem;
    }
    
    .user-info {
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .add-btn {
        width: 100%;
        padding: 0.75rem 1.5rem;
    }
}

@media (max-width: 480px) {
    .find-container {
        padding: 1rem 0.5rem;
    }
    
    h1 {
        font-size: 1.75rem;
    }
    
    .search-input {
        padding: 0.875rem 1.25rem;
        font-size: 1rem;
    }
}
</style>
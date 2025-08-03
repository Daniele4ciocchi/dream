<template>
    <div class="profile-container">
        <div class="profile-card">
            <div class="profile-header">
                <div class="avatar">
                    <span class="avatar-text">{{ userInitials }}</span>
                </div>
                <h2>👤 Il tuo Profilo</h2>
                <p class="welcome-text">Bentornato nel tuo spazio personale, {{ user?.username || 'Utente' }}!</p>
            </div>

            <div class="profile-content">
                <div class="info-section">
                    <h3>📋 Informazioni Personali</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>👤 Nome Utente</label>
                            <div class="info-value">{{ user?.username || 'N/A' }}</div>
                        </div>
                        <div class="info-item">
                            <label>📧 Email</label>
                            <div class="info-value">{{ user?.email || 'N/A' }}</div>
                        </div>
                        <div class="info-item">
                            <label>📅 Membro dal</label>
                            <div class="info-value">{{ formatDate(user?.created_at) }}</div>
                        </div>
                        <div class="info-item">
                            <label>🔄 Ultimo aggiornamento</label>
                            <div class="info-value">{{ formatDate(user?.updated_at) }}</div>
                        </div>
                        <div class="info-item">
                            <label>✅ Stato Account</label>
                            <div class="info-value">
                                <span class="status-badge" :class="{ active: user?.is_active }">
                                    {{ user?.is_active ? 'Attivo' : 'Non Attivo' }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="stats-section">
                    <h3>📊 Statistiche</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">{{ dreamCount }}</div>
                            <div class="stat-label">🌙 Sogni Salvati</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{{ daysSinceJoined }}</div>
                            <div class="stat-label">📆 Giorni con noi</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{{ averageDreamsPerWeek }}</div>
                            <div class="stat-label">📈 Sogni/Settimana</div>
                        </div>
                    </div>
                </div>

                <div class="actions-section">
                    <h3>⚙️ Azioni</h3>
                    <div class="action-buttons">
                        <button class="btn btn-primary" @click="editProfile">
                            ✏️ Modifica Profilo
                        </button>
                        <button class="btn btn-secondary" @click="changePassword">
                            🔒 Cambia Password
                        </button>
                        <button class="btn btn-info" @click="exportData">
                            📤 Esporta Dati
                        </button>
                        <button class="btn btn-danger" @click="confirmLogout">
                            🚪 Logout
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal di conferma logout -->
        <div v-if="showLogoutModal" class="modal-overlay" @click="closeLogoutModal">
            <div class="modal-content" @click.stop>
                <h3>🚪 Conferma Logout</h3>
                <p>Sei sicuro di voler uscire dal tuo account?</p>
                <div class="modal-actions">
                    <button class="btn btn-secondary" @click="closeLogoutModal">Annulla</button>
                    <button class="btn btn-danger" @click="logout">Conferma Logout</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useAuthStore } from '../utils/auth.js'
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api.js'

export default {
    name: 'UserProfile',
    setup() {
        const { getters, actions } = useAuthStore()
        const router = useRouter()
        const showLogoutModal = ref(false)
        const loading = ref(false)

        // Dati mock per quando non c'è utente reale
        const mockUser = {
            username: 'Demo User',
            email: 'demo@dreamkeeper.com',
            created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
            updated_at: new Date().toISOString(),
            is_active: true
        }

        // Stats mock
        const dreamCount = ref(42)
        const daysSinceJoined = ref(30)
        const averageDreamsPerWeek = ref(3.2)

        // ===== COMPUTED =====
        const user = computed(() => {
            // Se c'è un utente autenticato, usalo
            if (getters.user.value) {
                return getters.user.value
            }
            // Altrimenti usa i dati mock
            return mockUser
        })

        const userInitials = computed(() => {
            if (!user.value?.username) return 'DU'
            return user.value.username.substring(0, 2).toUpperCase()
        })

        // ===== METODI =====
        const loadUserData = async () => {
            // Solo se c'è un token prova a caricare i dati reali
            const token = localStorage.getItem('token')
            if (!token) {
                console.log('📋 Nessun token - usando dati demo')
                return
            }

            loading.value = true
            try {
                console.log('📡 Caricamento dati utente...')
                const response = await api.get('/api/auth/me')
                
                if (response.data.user) {
                    actions.updateUser(response.data.user)
                    console.log('✅ Dati utente caricati:', response.data.user.username)
                }
            } catch (error) {
                console.error('❌ Errore caricamento dati:', error.response?.data?.message || error.message)
                
                // Se errore 401, probabilmente token non valido
                if (error.response?.status === 401) {
                    console.log('🔑 Token non valido - usando dati demo')
                }
            } finally {
                loading.value = false
            }
        }

        const formatDate = (dateString) => {
            if (!dateString) return 'N/A'
            return new Date(dateString).toLocaleDateString('it-IT', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            })
        }

        const calculateDaysSinceJoined = () => {
            if (!user.value?.created_at) return 30
            const joinDate = new Date(user.value.created_at)
            const today = new Date()
            const diffTime = Math.abs(today - joinDate)
            return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
        }

        // Actions
        const editProfile = () => alert('Funzionalità in arrivo!')
        const changePassword = () => alert('Funzionalità in arrivo!')
        const exportData = () => alert('Funzionalità in arrivo!')
        const confirmLogout = () => showLogoutModal.value = true
        const closeLogoutModal = () => showLogoutModal.value = false
        
        const logout = () => {
            actions.logout()
            showLogoutModal.value = false
            router.push('/home')
        }

        // ===== LIFECYCLE =====
        onMounted(async () => {
            console.log('🏠 Profile montato')
            
            // Inizializza auth
            actions.init()
            
            // Carica dati utente se possibile
            await loadUserData()
            
            // Calcola giorni
            daysSinceJoined.value = calculateDaysSinceJoined()
        })

        return {
            user,
            userInitials,
            dreamCount,
            daysSinceJoined,
            averageDreamsPerWeek,
            showLogoutModal,
            loading,
            formatDate,
            editProfile,
            changePassword,
            exportData,
            confirmLogout,
            closeLogoutModal,
            logout,
            loadUserData
        }
    }
}
</script>

<style scoped>
.profile-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: calc(100vh - 120px);
    padding: 2rem;
    flex: 1;
}

.profile-card {
    background: #f7f6fa;
    border-radius: 16px;
    padding: 2rem;
    width: 100%;
    max-width: 800px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    border: 2px solid #4b2e83;
    color: #333 !important;
}

.profile-header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid #e0e0e0;
}

.avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    box-shadow: 0 4px 12px rgba(75, 46, 131, 0.3);
}

.avatar-text {
    color: white;
    font-size: 1.8rem;
    font-weight: bold;
}

.profile-header h2 {
    color: #4b2e83;
    margin-bottom: 0.5rem;
    font-size: 2rem;
}

.welcome-text {
    color: #666;
    font-size: 1.1rem;
    margin: 0;
}

.profile-content {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.info-section h3,
.stats-section h3,
.actions-section h3 {
    color: #4b2e83;
    margin-bottom: 1rem;
    font-size: 1.3rem;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}

.info-item {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}

.info-item label {
    display: block;
    font-weight: 600;
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.info-value {
    color: #333;
    font-size: 1rem;
}

.status-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    background: #e74c3c;
    color: white;
}

.status-badge.active {
    background: #4caf50;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
}

.stat-card {
    background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(75, 46, 131, 0.3);
}

.stat-number {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 0.9rem;
    opacity: 0.9;
}

.action-buttons {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.btn {
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
}

.btn-primary {
    background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
    color: white;
}

.btn-secondary {
    background: #6c757d;
    color: white;
}

.btn-info {
    background: #17a2b8;
    color: white;
}

.btn-danger {
    background: #dc3545;
    color: white;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Modal */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    max-width: 400px;
    width: 90%;
    text-align: center;
}

.modal-content h3 {
    color: #4b2e83;
    margin-bottom: 1rem;
}

.modal-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 1.5rem;
}

/* Responsive */
@media (max-width: 768px) {
    .profile-container {
        padding: 1rem;
    }

    .profile-card {
        padding: 1.5rem;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }

    .action-buttons {
        grid-template-columns: 1fr;
    }
}
</style>

<template>
  <div class="app">
    <div class="header">
      <div class="nav-item nav-item-left">
        <div class="nav-menu-item">
          <router-link class="logo" to="/home">DreamKeeper</router-link>
        </div>
        
      </div>

      <div class="nav-item nav-item-center">
        <ul class="nav-ul">
          <li class="nav-menu-item"><router-link to="/helloworld">Feed</router-link></li>
          <li class="nav-menu-item"><router-link to="/pomodoro">Pomodoro</router-link></li>
          <li class="nav-menu-item"><router-link to="/contact">My Dreams</router-link></li>
          
        </ul>
      </div>

      <div class="nav-item nav-item-right">
        <ul class="nav-ul">
          <li class="nav-menu-item"><router-link to="/login">Login</router-link></li>
          <li class="nav-menu-item"><router-link to="/register">Register</router-link></li>
          <li class="nav-menu-item">
            <router-link to="/login">
              <svg class="feather" id="Login">
                <use href="/feather-sprite-v4.29.0.svg#user"></use>
              </svg>
            </router-link>
          </li>
        </ul>
      </div>
    </div>

    <router-view />
  </div>
</template>


<script setup>



</script>

<style>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: calc(100vw - 60px);
  padding: 10px 20px;
  margin: 10px;

  /* NEW: evita che il centro si sposti se i lati crescono */
  position: relative;
}

/* NAV-ITEMS COME COLONNE */
.nav-item {
  display: flex;
  align-items: center;
  background-color: #4a2e832f;
  color: white;
  border: 2px solid #4a2e837e;
  border-radius: 12px;
  padding: 5px 10px;
}

/* LAYOUT BILANCIATO */
.nav-item-left,
.nav-item-right {
  flex: 0 0 auto;
  /* larghezza fissa */
}

.nav-item-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  /* oppure: */
  /* flex: 1; justify-content: center; */
}

.logo {
  text-decoration: none;
  color: white;
}

/* UL STILI */
.nav-ul {
  list-style: none;
  display: flex;
  gap: 20px;
  padding: 0;
  margin: 0;
}

.nav-menu-item {
  padding: 5px 10px;
  color: #a3a2a241;
  border: 2px solid transparent;
  /* <-- invisibile inizialmente */
  border-radius: 10px;
  transition: border 0.5s ease, background 0.5s ease;
}

.nav-menu-item:hover {
  background: rgba(128, 128, 128, 0.438);
  border: 2px solid #a3a2a241;
}

.nav-menu-item a {
  
  text-decoration: none;
  color: white;
}

.feather {
  width: 24px;
  height: 24px;
  fill: currentColor;
}
</style>

<template>
  <div id="app">
    <nav>
      <router-link to="/">HomePageLayout</router-link>
      <router-link to="/codeforces">CodeforcesLayout</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>
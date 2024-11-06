<template>
  <!-- ======= Top Bar ======= -->
  <div id="topbar" class="d-flex align-items-center fixed-top">
    <div class="container d-flex align-items-center justify-content-center justify-content-md-between">
      <div class="align-items-center d-md-flex">
        <a href="/" style="color: white; font-size: larger">
          <b>&lt;/&gt;</b> DCode
        </a>
      </div>
    </div>
  </div>

  <slot name="body"></slot>
  <slot name="form"></slot>


  <div class="visit-count">Visit Count: {{ visit_count }}</div>

  <!-- ======= Footer ======= -->
  <footer id="footer" style="padding-top: 0;">
    <header id="header" class="d-flex align-items-center" style="padding-top: 0; padding-bottom: 1rem;">
      <div class="container d-flex flex-column align-items-center">
        <div class="social-links text-center">
          <a class="github" href="https://github.com/guru-divine" target="__blank"><i
              class="bi bi-github"></i></a>
          <a class="instagram" href="https://www.instagram.com/the.free_guy/" target="__blank"><i
              class="bi bi-instagram"></i></a>
          <a class="linkedin" href="https://www.linkedin.com/in/divya-raj-iitkgp/" target="__blank"><i
              class="bi bi-linkedin"></i></a>
        </div>
      </div>
    </header>
    <div class="container">
      <div class="copyright">
        &copy; Copyright <strong><span>DCode</span></strong>. All Rights Reserved
      </div>
      <div class="credits">
        Designed by <a href="https://github.com/guru-divine" target="__blank">Divya Raj</a>
      </div>
    </div>
  </footer><!-- End #footer -->

  <a class="back-to-top d-flex align-items-center justify-content-center" href="#"><i
      class="bi bi-arrow-up-short"></i></a>
</template>

<script>
export default {
  name: 'BaseLayout',
  props: {
    visit_count: {
      type: String,
      required: true
    }
  }
};
</script>

<style scoped>
/* Your styles here */
</style>

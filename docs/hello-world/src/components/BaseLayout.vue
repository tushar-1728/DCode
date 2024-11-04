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

    <!-- <div style="height: 30px;"></div> -->
    <slot name="body"></slot>
    <slot name="form"></slot>


    <div class="visit-count">Visit Count: {{ visit_count }}</div>

    <!-- ======= Footer ======= -->
    <footer id="footer" style="padding-top: 0;">
        <header id="header" class="d-flex align-items-center" style="padding-top: 0; padding-bottom: 1rem;">
            <div class="container d-flex flex-column align-items-center">
                <div class="social-links text-center">
                    <a href="https://github.com/guru-divine" target="__blank" class="github"><i
                            class="bi bi-github"></i></a>
                    <!--<a href="https://www.facebook.com/profile.php?id=100023492681334" target="__blank" class="facebook"><i class="bi bi-facebook"></i></a>-->
                    <a href="https://www.instagram.com/the.free_guy/" target="__blank" class="instagram"><i
                            class="bi bi-instagram"></i></a>
                    <a href="https://www.linkedin.com/in/divya-raj-iitkgp/" target="__blank" class="linkedin"><i
                            class="bi bi-linkedin"></i></a>
                    <!--<a href="#" target="__blank" class="discord"><i class="bi bi-discord"></i></a>-->
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

    <a href="#" class="back-to-top d-flex align-items-center justify-content-center"><i
            class="bi bi-arrow-up-short"></i></a>

</template>

<script>
export default {
    name: 'BaseLayout',
    props: {
        visit_count: Number,
        required: true
    }
};
</script>

<style scoped>
/* Your styles here */
</style>

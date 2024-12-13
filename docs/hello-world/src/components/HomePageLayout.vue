<template>
    <BaseLayout visit_count="0">
        <template v-slot:body>
            <main id="main">
                <!-- ======= About Us Section ======= -->
                <section id="header" class="about">
                    <div class="container">
                        <div class="section-title">
                            <h2 style="font-size: 4rem;">DCode</h2>
                            <p>One Platform, Endless Possibilities</p>
                        </div>

                        <div class="row mt-2">
                            <div class="col-lg-4 col-md-6 mb-3" v-for="(item, index) in platforms" :key="index">
                                <a :href="item.link">
                                    <div class="icon-box"
                                        style="border: 5px solid #fff; border-radius: 10px; padding: 1rem;">
                                        <div class="icon">
                                            <img :src="item.image" style="width: 200px;" />
                                        </div>
                                        <h4 class="title" style="color: white;">{{ item.name }}</h4>
                                    </div>
                                </a>
                            </div>
                        </div>

                        <div style="height: 7rem"></div>
                        <div class="section-title">
                            <h3>View your Handle</h3>
                        </div>

                        <div class="row mt-2">
                            <div class="col-lg-4 col-md-6 mb-3" v-for="(item, index) in visualizers" :key="index">
                                <a :href="item.link">
                                    <div class="icon-box"
                                        style="border: 5px solid #fff; border-radius: 10px; padding: 1rem;">
                                        <div class="icon">
                                            <img :src="item.image" style="width: 200px;" />
                                        </div>
                                        <h4 class="title" style="color: white;">{{ item.name }}</h4>
                                    </div>
                                </a>
                            </div>
                        </div>
                    </div>
                </section><!-- End About Us Section -->
            </main><!-- End #main -->
            <div style="height: 2rem;"></div>
        </template>
    </BaseLayout>
</template>

<script>
import BaseLayout from './BaseLayout.vue';

export default {
    name: 'HomePageLayout',
    // props: {
    //     visit_count: {
    //         type: Number,
    //         required: true
    //     }
    // },
    components: {
        BaseLayout
    },
    mounted() {
        document.title = 'DCode';
    },
    data() {
        return {
            platforms: [
                { name: "Codeforces", link: "codeforces", image: "assets/img/code-forces.svg" },
                { name: "AtCoder", link: "atcoder", image: "assets/img/atcoder.png" },
                { name: "CodeChef", link: "codechef", image: "assets/img/codechef.svg" },
            ],
            visualizers: [
                { name: "Codeforces", link: "codeforces-visualizer", image: "assets/img/code-forces.svg" },
                { name: "AtCoder", link: "atcoder-visualizer", image: "assets/img/atcoder.png" },
                { name: "CodeChef", link: "codechef-visualizer", image: "assets/img/codechef.svg" },
            ],
        };
    },
};
</script>

<style scoped>
/* Your styles here */
</style>
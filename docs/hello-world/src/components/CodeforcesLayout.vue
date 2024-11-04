<template>
    <BaseLayout visit_count="0">
        <main id="main">
            <header id="header">
                <!-- Logo Section -->
                <div class="center-logo">
                    <img src="https://codeforces.com/codeforces.org/s/41923/images/codeforces-sponsored-by-ton.png" width="350px" alt="Codeforces Logo" />
                </div>

                <br />

                <div class="container d-flex flex-column align-items-center">
                    <!-- Form Section -->
                    <form @submit.prevent="submitForm">
                        <div class="subscribe" style="justify-content: flex-end;">
                            <div class="subscribe-form">
                                <input v-model="userHandle" type="text" placeholder="CF Handle"
                                    style="border: none; outline: none; background: none; padding-left:1rem;" />
                                <button type="submit">🔍</button>
                            </div>
                        </div>

                        <!-- Rating Slider -->
                        <div class="subscribe">
                            <button @click.prevent="prevSlide">Prev</button>
                            <div class="slider-container">
                                <div class="slides"
                                    :style="{ transform: `translateX(-${currentSlide * slideWidth}px)` }">
                                    <!-- Rating Groups -->
                                    <div v-for="(ratings, index) in ratingGroups" :key="index" class="slide">
                                        <button v-for="rating in ratings" :key="rating"
                                            :class="{ 'rating-btn': true, selected: probRating === rating }"
                                            @click.prevent="selectRating(rating)">
                                            {{ rating }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <button @click.prevent="nextSlide">Next</button>
                        </div>
                    </form>

                    <!-- User Info Section -->
                    <div class="user-info" v-if="userHandle">
                        <div class="user-info-cell" :style="{ color: ratingColor }">
                            <a :href="`https://codeforces.com/profile/${userHandle}`" :style="{ color: ratingColor }"
                                target="__blank">
                                <b>{{ userHandle }}</b> ({{ rank }})
                            </a>
                        </div>
                        <div class="user-info-cell">Rating: {{ rating }} (Max: {{ maxRating }})</div>
                        <div class="user-info-cell" style="color: #0FFF50">Solved: {{ correctCount }}</div>
                        <div class="user-info-cell" style="color: #F88379">Unsolved: {{ 100 - correctCount }}</div>
                    </div>

                    <!-- Tag Buttons -->
                    <div class="table-container">
                        <div class="text-sm flex flex-wrap m-3">
                            <button v-for="tag in tags" :key="tag" class="tag-btn"
                                :class="{ selected: selectedTags.includes(tag) }" @click="toggleTag(tag)">
                                {{ tag }}
                            </button>
                        </div>
                        <button @click="submitTags">Search</button>
                    </div>

                    <!-- Problems Table -->
                    <div class="table-container">
                        <div class="table-head">
                            <div class="table-cell">Index</div>
                            <div class="table-cell">Problem</div>
                            <div class="table-cell">Rating</div>
                            <div class="table-cell">Status</div>
                        </div>

                        <div v-for="(problem, index) in problems" :key="index" class="table-body">
                            <a :href="`https://codeforces.com/contest/${problem.contestId}/problem/${problem.index}`"
                                target="__blank">
                                <div class="table-cell" :style="{ color: getProblemColor(index) }">{{ index + 1 }}</div>
                                <div class="table-cell" :style="{ color: getProblemColor(index) }">{{ problem.name }}
                                </div>
                                <div class="table-cell" :style="{ color: getProblemColor(index) }">{{ problem.rating }}
                                </div>
                                <div class="table-cell" :style="{ color: getProblemColor(index) }">{{ getVerdict(index)
                                    }}
                                </div>
                            </a>
                        </div>
                    </div>
                </div>
            </header>
        </main>
    </BaseLayout>
</template>

<script>
import BaseLayout from './BaseLayout.vue';

export default {
    name: "CodeforcesPage",
    data() {
        return {
            userHandle: "",
            ratingGroups: [
                Array.from({ length: 10 }, (_, i) => 800 + i * 100),
                Array.from({ length: 10 }, (_, i) => 1800 + i * 100),
                Array.from({ length: 8 }, (_, i) => 2800 + i * 100),
            ],
            currentSlide: 0,
            probRating: null,
            tags: ["tag1", "tag2", "tag3"], // Example tags
            selectedTags: [],
            problems: [],
            ratingColor: "black",
            rank: "Specialist",
            rating: 0,
            maxRating: 0,
            correctCount: 50,
        };
    },
    computed: {
        slideWidth() {
            return 200; // Adjust based on slide width
        },
    },
    methods: {
        submitForm() {
            // Handle form submission logic
        },
        selectRating(rating) {
            this.probRating = rating;
        },
        prevSlide() {
            if (this.currentSlide > 0) {
                this.currentSlide--;
            }
        },
        nextSlide() {
            if (this.currentSlide < this.ratingGroups.length - 1) {
                this.currentSlide++;
            }
        },
        toggleTag(tag) {
            const index = this.selectedTags.indexOf(tag);
            if (index > -1) {
                this.selectedTags.splice(index, 1);
            } else {
                this.selectedTags.push(tag);
            }
        },
        submitTags() {
            // Submit selected tags to server or handle logic
        },
        getProblemColor(index) {
            return this.user_verdicts[index] === "AC" ? "#0FFF50" : this.user_verdicts[index] === "WA" ? "#F88379" : "white";
        },
        getVerdict(index) {
            return this.user_verdicts[index] || "-";
        },
    },
    mounted() {
        setInterval(() => {
            window.location.reload();
        }, 300000); // Refresh every 5 minutes
    },
};
</script>

<style scoped>
/* Your styles here */
</style>
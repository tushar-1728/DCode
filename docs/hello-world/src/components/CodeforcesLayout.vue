<template>
  <BaseLayout visit_count="0">
    <template v-slot:form>
      <main>
        <header id="header">
          <!-- Logo Section -->
          <div class="center-logo">
            <img alt="Codeforces Logo" src="assets/img/code-forces-logo.svg" width="350px" />
          </div>
          <br />
          <div class="container d-flex flex-column align-items-center">
            <!-- Form Section -->
            <form @submit.prevent="submitForm">
              <div class="subscribe" style="justify-content: flex-end;">
                <div class="subscribe-form">
                  <input v-model="userHandle" placeholder="CF Handle"
                    style="border: none; outline: none; background: none;" type="text"/>
                  <input type="submit" value="🔍"/>
                </div>
              </div>

              <!-- Rating Slider -->
              <div class="subscribe">
                <button @click.prevent="prevSlide">Prev</button>
                <div class="slider-container">
                  <div :style="{ transform: scrollStyle }" class="slides" ref="slides">
                    <!-- Rating Groups -->
                    <div v-for="(ratings, index) in ratingGroups" :key="index" class="slide" ref="slide">
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
            <div v-if="userHandle" class="user-info">
              <div :style="{ color: ratingColor }" class="user-info-cell">
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
            <div class="table-container" style="margin-bottom: 1rem; padding:0;">
              <div class="text-sm flex flex-wrap justify-items-start m-3 content-center">
                <button v-for="tag in tags" :key="tag" :class="{ selected: selectedTags.includes(tag) }" class="tag-btn"
                  @click="toggleTag(tag)">
                  {{ tag }}
                </button>
              </div>
              <div class="submit-tag">
                <button class="submit-tag-btn" @click="submitTags">Search</button>
              </div>
            </div>

            <!-- Problems Table -->
            <div class="table-container">
              <div class="table-head" style="margin-bottom: 1rem; border-radius: 0.5rem;">
                <div class="table-cell">Index</div>
                <div class="table-cell">Problem</div>
                <div class="table-cell">Rating</div>
                <div class="table-cell">Status</div>
              </div>

              <div v-for="(problem, index) in problems" :key="index">
                <a :href="`https://codeforces.com/contest/${problem.contestId}/problem/${problem.index}`"
                  target="__blank">
                  <div class="table-body" style="margin-bottom: 0.5rem; border-radius: 0.5rem;">
                    <div :style="{ color: getProblemColor(index) }" class="table-cell">{{ index }}</div>
                    <div :style="{ color: getProblemColor(index) }" class="table-cell">{{ problem.name }}</div>
                    <div :style="{ color: getProblemColor(index) }" class="table-cell">{{ problem.rating }}</div>
                    <div :style="{ color: getProblemColor(index) }" class="table-cell">{{ getVerdict(index) }}</div>
                  </div>
                </a>
              </div>
            </div>
            <!-- Problems Table Ends -->
          </div>
        </header>
      </main>
    </template>
  </BaseLayout>
</template>

<script>
import BaseLayout from './BaseLayout.vue';
import tagData from '@/assets/cf-problem-tags/tags.json';

export default {
  name: "CodeforcesPage",
  components: {
    BaseLayout
  },
  data() {
    return {
      userHandle: "",
      probRating: "1500",
      ratingGroups: [
        Array.from({ length: 10 }, (_, i) => 800 + i * 100),
        Array.from({ length: 10 }, (_, i) => 1800 + i * 100),
        Array.from({ length: 8 }, (_, i) => 2800 + i * 100),
      ],
      currentSlide: 0,
      tags: tagData.tags,
      selectedTags: [],
      problems: [],
      ratingColor: "black",
      rank: "Specialist",
      rating: 0,
      maxRating: 0,
      correctCount: 50,
      scrollStyle: ""
    };
  },
  watch: {
    probRating: 'fetchProblems',
    currentSlide: 'updateSlideWidth'
  },
  computed: {
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
    updateSlideWidth() {
      let slideWidth = this.$refs.slide[this.currentSlide].offsetWidth;
      this.scrollStyle = `translateX(-${this.currentSlide * slideWidth}px)`;
    },
    toggleTag(tag) {
      let index = this.selectedTags.indexOf(tag);
      if (index > -1) {
        this.selectedTags.splice(index, 1);
      } else {
        this.selectedTags.push(tag);
      }
    },
    submitTags() {
      // Submit selected tags to server or handle logic
      console.log('Tags sent to handle logic.');
    },
    getProblemColor(index) {
      index + 0
      // return this.user_verdicts[index] === "AC" ? "#0FFF50" : this.user_verdicts[index] === "WA" ? "#F88379" : "white";
      return "white"
    },
    getVerdict(index) {
      // return this.user_verdicts[index] || "-";
      index + 0
      return "-"
    },
    async fetchProblems() {
      try {
        if (this.probRating <= 1700)
          this.currentSlide = 0
        else if (this.probRating <= 2700)
          this.currentSlide = 1
        else
          this.currentSlide = 2
        this.problems = (await import(`@/assets/cf-rating-problems/${this.probRating}.json`))["default"];
      } catch (error) {
        console.error('Error fetching tags:', error);
      }
    }
  },
  mounted() {
    this.fetchProblems();
    window.addEventListener('resize', this.updateSlideWidth);
  },
};
</script>

<style scoped>
/* Your styles here */
.rating-btn.selected {
  background-color: #63809B;
  /* Change this to your desired highlight color */
  color: white;
}
</style>


<template>
  <div class="container columns-2">
    <draggable class="column" :list="folder1Images" group="images1" :move="checkMove" handle=".handle">
      <div class="image-container" v-for="(image, index) in folder1Images" :key="index">
        <div>{{index+1}}</div>
        <img :src="image.src" class="w-[200px]" :alt="image">
        <span class="handle">Drag</span>
        <button @click="moveToTop(index, 'folder1Images')">Move to Top</button>
      </div>
    </draggable>
    <draggable class="column" :list="folder2Images" group="images2" :move="checkMove" handle=".handle">
      <div class="image-container" v-for="(image, index) in folder2Images" :key="index">
        <img :src="image.src" class="w-[200px]" :alt="image">
        <span class="handle">Drag</span>
        <button @click="moveToTop(index, 'folder2Images')">Move to Top</button>
      </div>
    </draggable>
  </div>
  <div><button @click.prevent="submitMatches" class="border-2 border-blue-600 rounded-md p-2 bg-blue-600 text-bold text-white">Sort and rename</button></div>
  <div>{{outputtext}}</div>

</template>

<script>
import axios from 'axios';
import { VueDraggableNext } from 'vue-draggable-next';

export default {
  components: {
    draggable: VueDraggableNext,
  },
  data() {
    return {
      folder1Images: [], // Populate with image filenames from folder 1
      folder2Images: [], // Populate with image filenames from folder 2
      matches: {},
    };
  },
  computed: {
    outputtext: function() {
      var retval = {
        "one": this.folder1Images,
        "two": this.folder2Images
      }
      return retval;
    }
  },
  mounted() {
    this.fetchInitialFiles();
  },
  methods: {
    fetchInitialFiles() {
      axios.get('/initialfiles')
        .then(response => {
          // Assuming the response contains two arrays: files for column1 and column2
          this.folder1Images = response.data.one;
          this.folder2Images = response.data.two;
        })
        .catch(error => {
          console.error('There was an error fetching the initial files:', error);
        });
    },
    checkMove() {
      return true;
    },
    moveToTop(index, column) {
      if (column === 'folder1Images') {
        const item = this.folder1Images.splice(index, 1)[0];
        this.folder1Images.unshift(item);
      } else if (column === 'folder2Images') {
        const item = this.folder2Images.splice(index, 1)[0];
        this.folder2Images.unshift(item);
      }
    },
    getImagePath(filename) {
      // Implement logic to return the correct image path
    },
    submitMatches() {
      this.matches = this.folder2Images.reduce((acc, image, index) => {
        acc[image] = this.folder1Images[index];
        return acc;
      }, {});

      axios.post('/submit', { imageselection: this.outputtext })
        .then(response => {
          // Handle success
          alert('done! great job!');
          this.fetchInitialFiles();
        })
        .catch(error => {
          // Handle error
          alert('something went wrong')
        });
    },
  },
};
</script>


<style>
.column {
  display: flex;
  flex-direction: column;
}
.handle {
  cursor: grab;
}
.image-container {
  display: flex;
  align-items: center;
}
</style>
<template>
  <div>
    <div v-show="isLoading" class="text-center">
      <v-progress-circular
        indeterminate
        color="blue-gray"
      ></v-progress-circular>
    </div>
    <div v-show="!isLoading">
      <v-btn
        class="mx-2 d-none d-sm-flex"
        @click="$router.back()"
        fab
        fixed
        dark
        small
        color="blue-grey lighten-2"
      >
        <v-icon dark> mdi-arrow-left </v-icon>
      </v-btn>
      <v-row justify="center" align-content="center">
        <v-col class="py-0">
          <v-card
            elevation="5"
            shaped
            color="blue-grey lighten-5"
            class="mx-auto"
            max-width="1100px"
          >
            <div class="px-3">
              <v-row justify="center">
                <v-col cols="12" md="7">
                  <v-card-title
                    class="float-left text-lg-h4 text-xs-caption font-weight-bold"
                  >
                    {{ post.title }}
                  </v-card-title>
                  <div class="text-right">
                    <v-btn
                      class="px-0"
                      v-if="author.id"
                      text
                      :to="{ name: 'mypage', params: { user_id: author.id } }"
                      style="text-transform: none; text-decoration: none"
                    >
                      <v-avatar size="36px" class="ma-2">
                        <img :src="author.icon_image" />
                      </v-avatar>
                      <span class="text-lg-h6">
                        {{ author.username }}
                      </span>
                    </v-btn>
                    <div>
                      <span>{{ post.published_at | moment }}</span>
                    </div>
                    <div>
                      <span v-if="post.prefecture">{{ post.prefecture }}</span>
                      <span v-else>---</span>
                    </div>
                  </div>
                  <v-card-subtitle id="post_content">
                    {{ post.content }}
                  </v-card-subtitle>
                  <div uk-lightbox>
                    <a :href="post.raw_image">
                      <v-img eager id="post_image" :src="post.image"></v-img>
                    </a>
                  </div>
                  <div v-if="post.address">
                    <v-btn
                      class="px-10"
                      color="blue-grey lighten-2"
                      id="location_button"
                      :href="modal_href"
                      @click="showMap"
                      uk-toggle
                    >
                      <v-icon left> mdi-map-marker </v-icon>
                      場所を確認
                    </v-btn>
                    <div :id="modal" class="uk-modal-flex" uk-modal>
                      <div
                        id="location_modal"
                        class="uk-modal-dialog uk-modal-body uk-margin-auto-vertical"
                      >
                        <button
                          class="uk-modal-close-default"
                          type="button"
                          uk-close
                        ></button>
                        <div>
                          <Map ref="map" :post="post" />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div id="like_buttun">
                    <div v-if="isLiked">
                      <div>
                        <span @click="toggleLike" :disabled="isProcessing">
                          <v-btn class="ma-2" text icon color="red lighten-2">
                            <v-icon x-large>mdi-heart</v-icon>
                          </v-btn>
                        </span>
                        <span class="like_count">{{ likeCount }}</span>
                      </div>
                    </div>
                    <div v-else>
                      <div>
                        <span @click="toggleLike">
                          <v-btn class="ma-2" text icon>
                            <v-icon x-large>mdi-heart-outline</v-icon>
                          </v-btn>
                        </span>
                        <span class="like_count">{{ likeCount }}</span>
                      </div>
                    </div>
                  </div>
                </v-col>
                <v-col cols="12" md="5">
                  <div>
                    <div>
                      <CommentForm :post="post" @CommentGet="CommentGet" />
                    </div>
                  </div>
                  <div v-if="comments == ''">
                    <p id="none_message">まだコメントがありません</p>
                  </div>
                  <div v-else>
                    <div class="logbox">
                      <ul class="uk-comment-list">
                        <li v-for="comment in comments" :key="comment.id">
                          <article
                            class="uk-comment uk-comment-primary uk-visible-toggle"
                            tabindex="-1"
                          >
                            <header
                              class="uk-comment-header uk-position-relative"
                            >
                              <div>
                                <v-btn
                                  class="px-0 float-left"
                                  v-if="author.id"
                                  text
                                  :to="{
                                    name: 'mypage',
                                    params: { user_id: comment.author.id },
                                  }"
                                  style="
                                    text-transform: none;
                                    text-decoration: none;
                                  "
                                >
                                  <v-avatar size="36px" class="ma-2">
                                    <img :src="comment.author.icon_image" />
                                  </v-avatar>
                                  <span class="text-lg-h6">
                                    {{ comment.author.username }}
                                  </span>
                                </v-btn>
                                <div class="text-right text-body-2">
                                  <span>{{ comment.timestamp | moment }}</span>
                                </div>
                              </div>
                            </header>
                            <div>
                              <div>{{ comment.text }}</div>
                            </div>
                            <div
                              class="text-right"
                              v-if="comment.author.id == login_user_id"
                            >
                              <v-btn
                                text
                                icon
                                @click.stop="onClickBtn(comment)"
                              >
                                <v-icon>mdi-delete</v-icon>
                              </v-btn>
                              <v-dialog
                                v-model="dialog"
                                v-if="currentComment"
                                activator
                                max-width="600px"
                              >
                                <v-card class="pa-2">
                                  <v-card-title>削除確認</v-card-title>
                                  <v-card-text>
                                    コメント：{{
                                      currentComment.text
                                    }}を削除します。よろしいですか？</v-card-text
                                  >
                                  <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn @click="dialog = false">
                                      キャンセル
                                    </v-btn>
                                    <v-btn
                                      color="blue-grey lighten-3"
                                      @click="deleteComment(currentComment.id)"
                                      class="ml-4"
                                    >
                                      OK
                                    </v-btn>
                                  </v-card-actions>
                                </v-card>
                              </v-dialog>
                            </div>
                          </article>
                        </li>
                      </ul>
                    </div>
                  </div>
                </v-col>
              </v-row>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import CommentForm from "@/components/CommentForm";
import Map from "@/components/Map";
import api from "@/services/api";

export default {
  name: "detail",
  components: {
    CommentForm,
    Map,
  },
  filters: {
    moment: function (date) {
      return moment(date).format("YYYY年MM月DD日");
    },
  },
  props: ["post_id"],
  data() {
    return {
      comments: [],
      post: [],
      author: [],
      likeId: "",
      isLiked: false,
      likeCount: "",
      isLoading: true,
      isProcessing: false,
      dialog: false,
      currentComment: null,
    };
  },
  computed: {
    login_user_id() {
      return this.$store.getters["auth/id"];
    },
    isLoggedIn() {
      return this.$store.getters["auth/isLoggedIn"];
    },
    modal_href() {
      return "#" + "map_modal" + this.post.id;
    },
    modal() {
      return "map_modal" + this.post.id;
    },
  },
  mounted() {
    api.get("/posts/" + this.post_id + "/").then((response) => {
      this.author = response.data.author;
      this.post = response.data;
    });
    this.confirmLiked();
    this.getLikeCount();
    this.CommentGet();
  },
  methods: {
    async confirmLiked() {
      if (this.login_user_id) {
        await api
          .get("/likes/", {
            params: {
              author: this.login_user_id,
              post: this.post_id,
            },
          })
          .then((response) => {
            console.log(response.data.results);
            if (response.data.results[0]) {
              this.likeId = response.data.results[0].id;
              this.isLiked = true;
            }
          });
      }
    },
    getLikeCount() {
      api.get("/posts/" + this.post_id + "/").then((response) => {
        this.likeCount = response.data.likes_count;
        this.isLoading = false;
      });
    },
    toggleLike() {
      if (this.isLoggedIn) {
        if (this.isProcessing) return;
        this.isProcessing = true;
        this.isLiked ? this.removeLike() : this.addLike();
        return new Promise((resolve) => {
          setTimeout(() => {
            this.isProcessing = false;
            resolve();
          }, 500);
        });
      } else {
        this.$store.dispatch("message/setInfoMessage", {
          message: "ログインが必要です",
        });
        this.$router.replace("/login");
      }
    },
    addLike() {
      console.log("addLike");
      this.likeCount += 1;
      this.isLiked = true;
      this.confirmLiked;
      this.getLikeCount;
      api
        .patch("/posts/like/" + this.post_id + "/", {
          likes_count: this.likeCount,
        })
        .then(this.getLikeCount)
        .then(this.confirmLiked);
      api.post("/likes/", {
        author: this.login_user_id,
        post_id: this.post_id,
      });
    },
    removeLike() {
      console.log("removeLike");
      this.likeCount -= 1;
      this.isLiked = false;
      this.confirmLiked;
      this.getLikeCount;
      api
        .patch("/posts/like/" + this.post_id + "/", {
          likes_count: this.likeCount,
        })
        .then(this.getLikeCount)
        .then(this.confirmLiked);

      api.delete("/likes/" + this.likeId + "/");
    },
    CommentGet() {
      api.get("/comments/?post=" + this.post_id).then((response) => {
        this.comments = response.data;
      });
    },
    onClickBtn(comment) {
      this.currentComment = comment;
      this.dialog = true;
    },
    deleteComment(comment_id) {
      this.dialog = false;
      api.delete("/comments/" + comment_id + "/").then(this.CommentGet);
    },

    async showMap() {
      await this.$refs.map.initializeMap();
    },
    back() {
      // 1つ前へ
      this.$router.back();
    },
  },
};
</script>

<style scoped>
@import "../assets/common.css";

html {
  overflow: overlay;
}
.v-application ul,
.v-application ol {
  padding-left: 0px;
}
#post_content {
  word-break: break-all;
  margin: 0px 0px 10px 0px;
  padding: 5px 5px 5px 10px;
  font-size: 15px;
  white-space: pre-wrap;
}
#post_image {
  box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
}

#location_button {
  float: left;
  margin-top: 18px;
  text-decoration: none;
}
#like_buttun {
  max-width: 640px;
  text-align: right;
}

.like_count {
  font-size: 40px;
  position: relative;
  top: 8px;
}

.logbox {
  height: 520px;
  overflow-y: scroll;
  overflow-y: overlay;
}

#location_modal.uk-modal-dialog {
  position: relative;
  box-sizing: border-box;
  margin: 0 auto;
  width: 1000px;
  max-width: calc(100% - 0.01px) !important;
  background: rgb(240, 240, 240);
  transition: 0.3s linear;
  transition-property: opacity, transform;
}
#location_modal.uk-modal-body {
  display: flow-root;
  padding: 0px 0px;
  border-radius: 10px;
}

/* UIkitの上書き */

.uk-comment-primary {
  background-color: #fff;
  padding: 15px 15px 5px 15px;
  border-left: 4px solid black;
  border-bottom: 1px solid black;
}
.uk-comment-header {
  margin-bottom: 10px;
}

.uk-comment-list > :nth-child(n + 2) {
  margin-top: 0px;
}
ul.uk-comment-list {
  margin: 0;
}

@media (max-width: 640px) {
  #location_modal.uk-modal-body {
    display: flow-root;
    padding: 0px 0px;
    border-radius: 10px;
  }
}
</style>

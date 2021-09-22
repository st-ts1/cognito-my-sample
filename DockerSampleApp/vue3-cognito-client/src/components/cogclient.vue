<template>
  <div>
    REGION {{ REGION }}<br />
    USERPOOLID {{ USERPOOLID }}<br />
    CLIENTID {{ CLIENTID }}<br />
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "cogclient",
  props: {
    msg: String,
  },
  data: function () {
    return {
      REGION: "",
      USERPOOLID: "",
      CLIENTID: "",
    };
  },
  mounted: function () {
    var vm = this;
    console.log("mounted");
    vm.get_cog_info();
  },
  methods: {
    get_cog_info: function () {
      var vm = this;
      axios
        .get("http://192.168.56.103:8000/cog_info", {
          //headers: { Authorization: vm.loginpasswd },
          //params: {}
        })
        // thenで成功した場合の処理をかける
        .then((response) => {
          console.log("status:", response.status); // 200
          console.log(response.data); // response body.
          if (response.status != 200) {
            console.log("読み込み失敗");
            vm.$message({
              message: "読み込みエラー " + response.status,
              type: "error",
            });
          } else {
            vm.REGION = response.data.REGION;
            vm.USERPOOLID = response.data.USERPOOLID;
            vm.CLIENTID = response.data.CLIENTID;
          }
        })
        // catchでエラー時の挙動を定義する
        .catch((err) => {
          console.log("axios err:", err);
          console.log("ロード時に予期せぬエラー");
          vm.$message({
            message: "ロード時に予期せぬエラー",
            type: "error",
          });
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

<template>
  <div>
    <hr />
    REGION {{ REGION }}<br />
    USERPOOLID {{ USERPOOLID }}<br />
    CLIENTID {{ CLIENTID }}<br />
    <div>ユーザ</div>
    <el-input placeholder="Please input" v-model="user"></el-input>
    <div>パスワード</div>
    <el-input
      show-password
      placeholder="Please input"
      v-model="loginpasswd"
    ></el-input>
    <el-button v-on:click="auth_cog()">認証</el-button>
    <hr />
    accessToken {{ accessToken }}<br />
    idToken {{ idToken }}<br />
        <el-button v-on:click="call_api()">API呼び出し</el-button>
    <hr />
  </div>
</template>

<script>
import axios from "axios";
import {
  CognitoUserPool,
  AuthenticationDetails,
  CognitoUser,
} from "amazon-cognito-identity-js";
//import * as AWS from 'aws-sdk/global';
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
      user: "",
      loginpasswd: "",
      accessToken: "", // Cognitoのアクセストークン
      idToken: "", // Cognitoのidトークン
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
        .get(process.env.VUE_APP_API_URL+"/cog_info", {
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
    auth_cog: function () {
      let vm = this;
      console.log("handleClose");

      // Cognitoで認証する
      // 参考: https://github.com/aws-amplify/amplify-js/tree/master/packages/amazon-cognito-identity-js
      var authenticationData = {
        Username: vm.user,
        Password: vm.loginpasswd,
      };
      var authenticationDetails = new AuthenticationDetails(authenticationData);
      var poolData = {
        // ここを書き換える
        UserPoolId: vm.USERPOOLID, // Your user pool id here
        ClientId: vm.CLIENTID, // Your client id here
      };
      var userPool = new CognitoUserPool(poolData);
      var userData = {
        Username: vm.user,
        Pool: userPool,
      };
      var cognitoUser = new CognitoUser(userData);
      cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function (result) {
          var accessToken = result.getAccessToken().getJwtToken();
          // 追加した
          vm.accessToken = accessToken;
          // 追加した。アクセストークンとidTokenがある。
          var idToken = result.getIdToken().getJwtToken();
          vm.idToken = idToken;
          vm.$message("アクセストークン取得");
          console.log(accessToken);
          vm.loginVisible = false;
          return; // ここ以降はIDプール用な気がした

          //POTENTIAL: Region needs to be set if not already set previously elsewhere.
          // ここを書き換える
          /*
          AWS.config.region = "us-west-2";

          AWS.config.credentials = new AWS.CognitoIdentityCredentials({
            // ここを書き換える
            IdentityPoolId: "...", // your identity pool id here
            Logins: {
              // Change the key below according to the specific region your user pool is in.
              "cognito-idp.<region>.amazonaws.com/<YOUR_USER_POOL_ID>": result
                .getIdToken()
                .getJwtToken(),
            },
          });

          //refreshes credentials using AWS.CognitoIdentity.getCredentialsForIdentity()
          AWS.config.credentials.refresh((error) => {
            if (error) {
              console.error(error);
            } else {
              // Instantiate aws sdk service objects now that the credentials have been updated.
              // example: var s3 = new AWS.S3();
              console.log("Successfully logged!");
            }
          });
          */
        },

        onFailure: function (err) {
          alert(err.message || JSON.stringify(err));
        },
      });
    },
    call_api: function () {
      let vm = this;
      axios
        .get(process.env.VUE_APP_API_URL+"/checkjwt", {
          headers: { Authorization: vm.idToken },
          params: {}
        })
        // thenで成功した場合の処理をかける
        .then((response) => {
          console.log("status:", response.status); // 200
          console.log(response.data); // response body.
          if (response.status != 200) {
            console.log("API失敗");
            vm.$message({
              message: "APIエラー " + response.status,
              type: "error",
            });
          } else {
                        console.log("API失敗");
            vm.$message({
              message: "API成功",
              type: "success",
            });
          }
        })
        // catchでエラー時の挙動を定義する
        .catch((err) => {
          console.log("axios err:", err);
          console.log("API時に予期せぬエラー");
          vm.$message({
            message: "API時に予期せぬエラー",
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

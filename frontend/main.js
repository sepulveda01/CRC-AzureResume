window.addEventListener("DOMContentLoaded", (event) => {
  getCount();
});
//when HTML gets loaded, event gets fired up and function gets called

// const myAPIUrl =
//   "https://myresumemain.azurewebsites.net/api/MyCounterFunc?code=PZGbUruoS1i0mQFffnUr5qvDRXVOA8n5wHipaTSg_HDFAzFuuwIxyA==";
const functionApi = 'https://REPLACE_WITH_YOUR_FUNCTION_APP_NAME.azurewebsites.net/api/counter';
let count = 0;

const getCount = () => {
  fetch(functionApi)
    .then((res) => {
      return res.json();
    })
    .then((res) => {
      console.log(res);
      console.log("it's up and running");

      count = res.count;
      console.log(count);
      document.getElementById("visit_count").innerHTML = count;
    })
    .catch(function (error) {
      console.log(error);
    });
};

console.log(window);
// window.alert(1);
// window.alert(1);

// Single element
const form = document.getElementById("my-form");
console.log(form);
console.log(document.getElementById("my-form"));
console.log(document.querySelector("form")); // Only select the first one
console.log(document.querySelector(".container"));
console.log(document.querySelector("h1"));

// Multiple element
console.log(document.querySelectorAll(".item"));

// Loop thru items
const items = document.querySelectorAll(".items");
console.log("===");
items.forEach((item) => console.log(item));

// Manipulate the DOM
const ul = document.querySelector(".items");

// ul.remove();
// ul.lastElementChild.remove();
ul.firstElementChild.textContent = "Hello";
ul.children[1].innerText = "Brad";
ul.lastElementChild.innerHTML = "<h1>Hello</h1>";

const btn = document.querySelector(".btn");
btn.style.background = "red";

// Event
console.clear();
// btn.addEventListener("click", (e) => {
// hover
// btn.addEventListener("mouseover", (e) => {
// mouse moves out of button
btn.addEventListener("mouseout", (e) => {
  // btn.addEventListener("click", (e) => {
  e.preventDefault();
  // console.log("click");
  console.log(e);
  console.log(e.target);
  console.log(e.target.className);
  document.querySelector("#my-form").style.background = "#ccc";
  document.querySelector("body").classList.add("bg-dark");
  // document.querySelector(".item").lastElementChild.innerHTML =
  //   "<h1>Hello_1</h1>";
  // document.querySelector(".items li:last-child").innerHTML = "<h1>Hello_2</h1>";
  document.querySelector("li.item:last-child").innerHTML = "<h1>Hello_3</h1>";
});
// li.item:nth-child(3)

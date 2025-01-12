// https://developer.mozilla.org/en-US/docs/Web/API/console

// alert("Hello World!");
// console.log("Hello World, consol.log");
// console.error("This is an error");
// console.warn("This is a warning");

// values: let const

// let age=30;
// console.log(age);

// const age_const=40;
// console.log(age_const);

// age_const = 41;  // error

// data type: Sting, Number, Boolean, null, undefine, Symbols

const name = "John";
const age = 30;
const rating = 4.5;
const isCool = true;
const x = null;
const y = undefined;
let z;

// console.log(typeof name);
// console.log(typeof age);
// console.log(typeof rating);
// console.log(typeof isCool);
// console.log(typeof x);
// console.log(typeof y);
// console.log(typeof z);
// console.log("Hello");

// Concatenation
console.log("My name is " + name + " and my age is " + age);
// Template Sting
console.log(`My name is ${name} and my age is ${age}`);

const hello = `My name is ${name} and my age is ${age + 10}`;
console.log(hello);

console.log("======");
const s = "Hello World";
console.log(s.length); // Property does not have parenthesis
console.log(s.toLocaleUpperCase()); // Method has parentheses
console.log(s.substring(1, 6).toLocaleUpperCase());

const t = "technology, computer, IT";
console.log(t.split(", "));

// Comment
/*
Multi-line
comments
*/
// Arrays [ ]
const stuff = ["apples", "oranges", 10, true];
console.log(stuff);
console.log(stuff[1]); // return value in array
stuff[6] = "grapes";
console.log(stuff);
stuff.push("managos"); // Add to the end
console.log(stuff);
stuff.unshift("strawberries"); // Add to the beginning
console.log(stuff);
stuff.pop(); // Removes the last item
console.log(stuff);

console.log(Array.isArray(stuff)); // Test for array type
console.log(stuff);
console.log(stuff.indexOf("oranges"));

// Objects { }, similar to python dictionary
const person = {
  firstName: "John",
  lastName: "Doe",
  age: 30,
  hobbies: ["music", "movies", "sports"],
  address: {
    street: "50 main st",
    city: "Boston",
    state: "MA",
  },
};
console.log(person);
console.log(person.firstName, person.address, person.age);
console.log(person.hobbies[1]); // Get value in array
console.log(person.address.city); // Get value in object

// Get value from object
const {
  firstName,
  lastName,
  address: { city },
} = person;
console.log(firstName);
console.log(lastName);
console.log(city);

person.email = "john@gmail.com"; // Add to object
console.log(person);

// Array of objects
const todos = [
  {
    id: 1,
    text: "Take out trash",
    isComplete: true,
  },
  {
    id: 2,
    text: "Meeting with boss",
    isComplete: true,
  },
  {
    id: 1,
    text: "Dentist appt",
    isComplete: false,
  },
];
console.log(todos);
console.log(todos[1].text); // Get value of object inside array

// https://www.freeformatter.com/json-formatter.html
// [
//   {
//     id: 1,
//     text: "Take out trash",
//     isComplete: true,
//   },
//   {
//     id: 2,
//     text: "Meeting with boss",
//     isComplete: true,
//   },
//   {
//     id: 1,
//     text: "Dentist appt",
//     isComplete: false,
//   },
// ];

// Convert object to JSON to send to server
const todoJSON = JSON.stringify(todos);
console.log(todoJSON);

// For loop
for (let i = 0; i < 10; i++) {
  console.log(`For loop number: ${i}`);
}

// While loop
let i = 0;
while (i < 10) {
  console.log(`While loop number: ${i}`);
  i++;
}

// Loop thru object
const todos2 = [
  {
    id: 1,
    text: "Take out trash",
    isComplete: true,
  },
  {
    id: 2,
    text: "Meeting with boss",
    isComplete: true,
  },
  {
    id: 1,
    text: "Dentist appt",
    isComplete: false,
  },
];
for (let i = 0; i < todos2.length; i++) {
  console.log(`Item in todos2 object: ${i}`);
  console.log(`Item's text: ${todos2[i].text} `);
}
for (let todo of todos2) {
  console.log(todo.text);
}

// forEach
todos2.forEach(function (item) {
  console.log(`forEach item.text: ${item.text}`);
});

// map returns an array
const todoText = todos2.map(function (item) {
  return item.text;
});
console.log(todoText);

// filter
const todoCompleted = todos2.filter(function (item) {
  return item.isComplete == true;
});
console.log(todoCompleted);
// filter chain
const todoCompletedChain = todos2
  .filter(function (item) {
    return item.isComplete == true;
  })
  .map(function (item) {
    return item.text;
  });
console.log(todoCompletedChain);

// Variables

const a = 10;
if (a === 10) {
  console.log(`${a} is a ${typeof a}. a is the number 10`);
} else {
  console.log(`${a} is a ${typeof a}. a is Not the number 10`);
}

const b = 5;
if (b === 10) {
  console.log(`${b} is 10`);
} else if (b > 10) {
  console.log(`${b} is greater than 10`);
} else {
  console.log(`${b} is less than 10`);
}

if (a > 2 || b < 10) {
  console.log(`${a} > 2 or ${b} <10`);
} else if (a < 10 && b < 5) {
  console.log(`${a} < 10 and  ${b} < 5`);
}

// ternary operator ?, shorthand if operator
const c = 11;
const color = c > 10 ? "red" : "blue";
console.log(color);

// switch
switch (color) {
  case "red":
    console.log("color is red");
    break;
  case "blue":
    console.log("color is blue");
    break;
  default:
    console.log("color is Not red or blue");
    break;
}

// function
function addNums(num1 = 1, num2 = 2) {
  // console.log(num1 + num2);
  return num1 + num2;
}

addNums(10, 20);
console.log(addNums(100, 200));

// arrow function
const addNums2 = (num1) => num1 + 1000;
console.log(addNums2(2));

const addNums3 = (num1 = 1, num2 = 2) => num1 + num2;
console.log(addNums3(2, 5));

// forEach
todos2.forEach(function (item) {
  console.log(`forEach item.text: ${item.text}`);
});
todos2.forEach((item) => console.log(item));
todos2.forEach((item) => console.log(item.text));

// // Constructor function, Objects
// function Person(firstName, lastName, dob) {
//   this.firstName = firstName;
//   this.lastName = lastName;
//   // this.dob = dob;
//   this.dob = new Date(dob);
//   // this.getBirthYear = function () {
//   //   return this.dob.getFullYear();
//   // };
//   // this.getFullName = function () {
//   //   return `${this.firstName} ${this.lastName}`;
//   // };
// }

// // prototype
// Person.prototype.getBirthYear = function () {
//   return this.dob.getFullYear();
// };

// Person.prototype.getFullName = function () {
//   return `${this.firstName} ${this.lastName}`;
// };

// Class
class Person {
  constructor(firstName, lastName, dob) {
    this.firstName = firstName;
    this.lastName = lastName;
    this.dob = new Date(dob);
  }
  getBirthYear() {
    return this.dob.getFullYear();
  }
  getFullName() {
    return `${this.firstName} ${this.lastName};`;
  }
}

// Instantiate object
const person1 = new Person("John", "Doe", "4-3-1980");
const person2 = new Person("Joan", "Smith", "5-4-1981");

console.log(person1);
console.log(person2.lastName);
console.log(person2.getBirthYear());
console.log(typeof person2.getBirthYear());
console.log(person1.getBirthYear());
console.log(person2.getFullName());

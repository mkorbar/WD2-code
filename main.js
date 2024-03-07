


// string
let name = 'Matej';

// number
let height = 180;

// boolean
let male = true;

// undefined
let kidName;

// null
let favoriteColor = null;

// should throw an error
// name = 'Janez';
/*

console.log(name);
console.log(height);
console.log(male);
console.log(kid_name);
console.log(favorite_color);

console.log('-----------------------------------');

console.log(typeof name);
console.log(typeof height);
console.log(typeof male);
console.log(typeof kid_name);
console.log(typeof favorite_color);


*/


/**
 * 
 * Objects
 * 
 */

// let person = {
//     name: 'Janez',
//     age: 12,
//     1: 'test value',
// }

// console.log(typeof person);
// console.log(person);
// console.log(person.name);

// parameter = 'name'

// console.log(person[parameter]);
// console.log(person.parameter);



/**
 * 
 * Array
 * 
 */

// var test = Array('test', 1 , true)

// let towns = ['Reka', 'Postojna', 'Ljubljana'];

// console.log(typeof towns);

// console.log(towns[0]);

// console.log(towns.length);


// ----------------------------------------------
/**
 * 
 * funckije
 * 
 */

// function say_hello(name = 'World') {
//     console.log('Hello ' + name);
// }

// say_hello()


// function calculate_consumption(consumption, gasVolume) {
//     return gasVolume / consumption * 100
// }

// console.log(calculate_consumption(7, 50));



/**
 * 
 * conditionals
 * 
*/

// const MIN_AGE = 18;
// let age = prompt('What\' your age again?', '99') * 1;

// if (age >= MIN_AGE) {
// 	console.log("sex, drugs and rock'n'roll");
// } else {
// 	console.log("rock'n'roll only");
// }

// let agree = confirm('Do you consent with bad humor');
// let badJoke = 'Q: Why is 6 afraid of 7? A: Because 7 eight 9';
// let noJoke = 'No joke for you!'

// agree ? console.log(badJoke) : console.log(noJoke)



switch (new Date().getDay()) {
    case 0:
      day = "Sunday";
      break;
    case 1:
      day = "Workonday";
      break;
    case 2:
       day = "Workesday";
      break;
    case 3:
      day = "Workednesday";
      break;
    case 4:
      day = "Workrsday";
      break;
    case 5:
      day = "Friday woooohooo!";
      break;
    case 6:
      day = "Saturday";
  }

  switch (new Date().getDay()) {
    case 4:
    case 5:
      text = "Just a bit more ...";
      break;
    case 0:
    case 6:
      text = "Wooho, weekend";
      break;
    default:
      text = "Urrrggghhhhhh!";
  }


let i = 99;

while (i > 0) {
  text += i + ' bottles of beer on the wall ' + i + ' bottles of beer, ...';
  i--;
}


let hills = ['Boč', 'Nanos', 'Krim', 'Plešivec', 'Krvavec', 'Kum']

// for (let i = 0; i < hills.length; i++) {
//   text += hills[i] + "<br>";
// } 

// for ( let i in hills) {
//     console.log(hills[i]);
// }

for ( let hill of hills) {
    console.log(hill);
}

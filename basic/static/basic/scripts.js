function populate_uniprot(){
    document.getElementById('input_uni').value="Q9BYF1";
    document.getElementById('input_var').value="199";
}


//Sticky header
//When the user scrolls the page, execute stickyHead
window.onscroll = function() {stickyHead()};

//Get the header
var header = document.getElementById("stick-to-top");

//Get the offset position of the navbar
var sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function stickyHead() {
    if (window.pageYOffset > sticky) {
      header.classList.add("sticky");
    } else {
      header.classList.remove("sticky");
    }
  };



// 1

// //Create a JavaScript string containing JSON sythax
// let test = '{"interactors": [' +
//   '{"uniprot_p1": "P84085", "uniprot_p2": "Q14123"},' +
//   '{"uniprot_p1": "P84085", "uniprot_p2": "Q13177"},' +
//   '{"uniprot_p1": "P84085", "uniprot_p2": "O95755"} ]}';

// //Use the JavaScript built-in function JSON.parse() to convert the string into a JavaScript object:
// const obj = JSON.parse(test);

// //Create empty network with styles
// var cy = cytoscape({
//   container: document.getElementById('cy'),
//   style: [
//     {
//       selector: 'node',
//       style: {
//           shape: 'hexagon',
//           'background-color': 'red',
//           label: 'data(id)'
//       }
//     }],
//   elements: [
//     ]
// });

// //Add nodes and edges using a loop
// for (var i = 0; i < obj.interactors.length; i++) {
//   cy.add(
//     { data: { id: obj.interactors[i].uniprot_p1 } }
//   );
//   cy.add(
//     { data: { id: obj.interactors[i].uniprot_p2 } }
//   );
//   cy.add(
//     { data: { id: i, source: obj.interactors[i].uniprot_p1, target: obj.interactors[i].uniprot_p2 } }
//   )
// };

// //Change layout
// cy.layout({
//   name: 'circle'
// });



// //2

// let test2 = document.getElementById('interaction-data').textContent;
// // remove all backward slashes
// let test3 = test2.replaceAll('\\','');
// // remove boundary quotation marks 
// let test4 = test3.replace(/^"|"$/g, '');
// const obj = JSON.parse(test4);


// //Create empty network with styles
// var cy = cytoscape({
//   container: document.getElementById('cy'),
//   style: [
//     {
//       selector: 'node',
//       style: {
//           shape: 'ellipse',
//           'border-width': 4,
//           'border-color': 'red',
//           'background-color': '#ffffff',
//           label: 'data(id)'
//       }}, 
//       {
//         selector: "edge",
//         style: {
//           width: 4}}, 
//       {
//         selector: "edge[exp > 0]",
//         style: {
//           "line-color": "red"}
//     }],
//   elements: [
//     ]
// });

// //Add nodes and edges using a loop
// for (var i = 0; i < obj.interactors.length; i++) {
//   cy.add(
//     { data: { id: obj.interactors[i].p1 } }
//   );
//   cy.add(
//     { data: { id: obj.interactors[i].p2 } }
//   );
//   cy.add(
//     { data: { id: i, 
//       source: obj.interactors[i].p1, 
//       target: obj.interactors[i].p2,
//       exp: obj.interactors[i].exp, } }
//   )
// };

// //Change layout
// cy.layout({
//   name: 'concentric'
// });




// 3 Use external data and style files

// Promise.all([
//   fetch('/static/basic/cy-style.json')
//     .then(function(res){
//       return res.json()
//     }),
//   fetch('/static/basic/data.json')
//     .then(function(res) {
//       return res.json()
//   })
// ])
//   .then(function(dataArray) {
//     var cy = cytoscape({
//       container: document.getElementById('cy'),
//       layout: {
//         name: 'concentric'
//       },
//       style: dataArray[0],
//       elements: dataArray[1]
//     });
//   });



//4 Cleans up codes from 2 and adopt 3

function convertJson(cont) {
  var cont_strip = cont.replaceAll('\\','').replace(/^"|"$/g, '')
  return JSON.parse(cont_strip)
}
const obj = convertJson(document.getElementById('interaction-data').textContent);

Promise.all([
  fetch('/static/basic/cy-style.json')
  .then(function(res) {
    return res.json()
  })
])
  .then(function(dataArray) {
    var cy = cytoscape({
      container: document.getElementById('cy'),
      style: dataArray[0],
      elements: [],
      });
    for (var i = 0; i < obj.interactors.length; i++) {
      cy.add(
        { data: { id: obj.interactors[i].p1, "idInt": i } }
      );
      cy.add(
        { data: { id: obj.interactors[i].p2 } }
      );
      cy.add(
        { data: { id: i, 
          source: obj.interactors[i].p1, 
          target: obj.interactors[i].p2,
          exp: obj.interactors[i].exp} }
      );
      if (obj.interactors[i].type != null) {
        cy.add(
          { data: { id: "i3d_" + i, 
            source: obj.interactors[i].p1, 
            target: obj.interactors[i].p2,
            type: obj.interactors[i].type} }
        );
      }
    };
    cy.layout({
      name: 'cose'
    });

  });








function populate_uniprot(){
    document.getElementById('input_uniprot').value="Q9BYF1";
    document.getElementById('input_residue').value="199";
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
  }





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
//     { data: { id: obj.interactors[0].uniprot_p1 } },
//     { data: { id: obj.interactors[1].uniprot_p1 } },
//     { data: { id: obj.interactors[2].uniprot_p1 } },
//     { data: { id: obj.interactors[0].uniprot_p2 } },
//     { data: { id: obj.interactors[1].uniprot_p2 } },
//     { data: { id: obj.interactors[2].uniprot_p2 } },
//     { data: { id: '1', source: obj.interactors[0].uniprot_p1, target: obj.interactors[0].uniprot_p2 } },
//     { data: { id: '2', source: obj.interactors[1].uniprot_p1, target: obj.interactors[1].uniprot_p2 } },
//     { data: { id: '3', source: obj.interactors[2].uniprot_p1, target: obj.interactors[2].uniprot_p2 } }
//   ]
// });



// // 3 

// Promise.all([
//   fetch('cy-style.json')
//     .then(function(res){
//       return res.json()
//     }),
//   fetch('data.json')
//     .then(function(res) {
//       return res.json()
//   })
// ])
//   .then(function(dataArray) {
//     var cy = window.cy = cytoscape({
//       container: document.getElementById('cy'),
//       layout: {
//         name: 'concentric'
//       },
//       style: dataArray[0],
//       elements: dataArray[1]
//     });
//   });


// 4

//Create a JavaScript string containing JSON sythax
let test = '{"interactors": [' +
'{"uniprot_p1": "P84085", "uniprot_p2": "Q14123", "type": "structure"},' +
'{"uniprot_p1": "P84085", "uniprot_p2": "Q13177", "type": "model"},' +
'{"uniprot_p1": "P84085", "uniprot_p2": "O95755", "type": "none"} ]}';

//Use the JavaScript built-in function JSON.parse() to convert the string into a JavaScript object:
const obj = JSON.parse(test);

//Create empty network with styles
var cy = cytoscape({
container: document.getElementById('cy'),
style: [
  {
    selector: 'node',
    style: {
        shape: 'hexagon',
        'background-color': 'red',
        label: 'data(id)' }
  }, {
    selector: 'edge[type=\"structure\"]',
    style: {
      "line-color": "green"
      } 
    }
  ],
elements: [
  ]
});

//Add nodes and edges using a loop
for (var i = 0; i < obj.interactors.length; i++) {
cy.add(
  { data: { id: obj.interactors[i].uniprot_p1 } }
);
cy.add(
  { data: { id: obj.interactors[i].uniprot_p2 } }
);
cy.add(
  { data: { id: i, 
    source: obj.interactors[i].uniprot_p1, 
    target: obj.interactors[i].uniprot_p2,
    type: obj.interactors[i].type,} }
)
};

//Change layout
cy.layout({
name: 'concentric'
});

function populate_uniprot(){
    document.getElementById('input_uni').value="Q9BYF1";
    document.getElementById('input_var').value="199";
}


// //Sticky header
// //When the user scrolls the page, execute stickyHead
// window.onscroll = function() {stickyHead()};

// //Get the header
// var header = document.getElementById("stick-to-top");

// //Get the offset position of the navbar
// var sticky = header.offsetTop;

// // Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
// function stickyHead() {
//     if (window.pageYOffset > sticky) {
//       header.classList.add("sticky");
//     } else {
//       header.classList.remove("sticky");
//     }
//   };



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



// //4 Cleans up codes from 2 and adopt 3

// function convertJson(cont) {
//   var cont_strip = cont.replaceAll('\\','').replace(/^"|"$/g, '')
//   return JSON.parse(cont_strip)
// }
// const obj = convertJson(document.getElementById('interaction-data').textContent);

// Promise.all([
//   fetch('/static/basic/cy-style.json')
//   .then(function(res) {
//     return res.json()
//   })
// ])
//   .then(function(dataArray) {
//     var cy = cytoscape({
//       container: document.getElementById('cy'),
//       style: dataArray[0],
//       elements: [],
//       });
//     for (var i = 0; i < obj.interactors.length; i++) {
//       cy.add(
//         { data: { id: obj.interactors[i].p1, "idInt": i } }
//       );
//       cy.add(
//         { data: { id: obj.interactors[i].p2 } }
//       );
//       cy.add(
//         { data: { id: i, 
//           source: obj.interactors[i].p1, 
//           target: obj.interactors[i].p2,
//           exp: obj.interactors[i].exp} }
//       );
//       if (obj.interactors[i].type != null) {
//         cy.add(
//           { data: { id: "i3d_" + i, 
//             source: obj.interactors[i].p1, 
//             target: obj.interactors[i].p2,
//             type: obj.interactors[i].type} }
//         );
//       }
//     };
//     cy.layout({
//       name: 'cose'
//     });

//   });







//5 Single edges (interactome3D or string)

// function convertJson(cont) {
//   var cont_strip = cont.replaceAll('\\','').replace(/^"|"$/g, '')
//   return JSON.parse(cont_strip)
// }
// const obj = convertJson(document.getElementById('interaction-data').textContent);

// Promise.all([
//   fetch('/static/basic/cy-style.json')
//   .then(function(res) {
//     return res.json()
//   })
// ])
//   .then(function(dataArray) {
//     var cy = window.cy = cytoscape({
//       container: document.getElementById('cy'),
//       style: dataArray[0],
//       elements: [],
//       });
//     for (var i = 0; i < obj.interactors.length; i++) {
//       cy.add(
//         { data: { id: obj.interactors[i].p1, 
//                   idInt: i,
//                   gene: obj.interactors[i].p1_gene} }
//       );
//       cy.add(
//         { data: { id: obj.interactors[i].p2,
//                   gene: obj.interactors[i].p2_gene } }
//       );
//       cy.add(
//         { data: { id: i, 
//           source: obj.interactors[i].p1, 
//           target: obj.interactors[i].p2,
//           exp: obj.interactors[i].exp,
//           type: obj.interactors[i].type} }
//       );
//     };
//     cy.layout({
//       name: 'cose'
//     });

//   });


//6 Add interactors only once to avoid error, deleted 'interactors'

function convertJson(cont) {
  var cont_strip = cont.replaceAll('\\','').replace(/^"|"$/g, '')
  return JSON.parse(cont_strip)
}
const cyData = convertJson(document.getElementById('interaction-data').textContent);

$('.node-operation').hide();

var selectedNodeHandler = function(evt) {
  $('.node-operation').show();
  var node_id = evt.cyTarget.id();
  $(".node-operation").text("Node selected: " + node_id);
}
var unselectedNodeHandler = function() {
  $('.node-operation').hide();
}
var selectededgeHandler = function(evt) {
  $('.edge-operation').show();
  var edge_id = evt.cyTarget.id();
  $(".edge-operation").text("Edge selected: " + cyData[edge_id].p1 + '_' + cyData[edge_id].p2);
  $(".edge-operation").append(`<p>Experimental evidence score: ${cyData[edge_id].exp}</p>
                              <p>Model/structure: ${cyData[edge_id].type}</p>`);
}
var unselectededgeHandler = function() {
  $('.edge-operation').hide();
}

Promise.all([
  fetch('/static/m3di/cy-style.json')
  .then(function(res) {
    return res.json()
  })
])
  .then(function(dataArray) {
    var cy = window.cy = cytoscape({
      container: document.getElementById('cy'),
      style: dataArray[0],
      elements: [],
      minZoom: 0.5,
      maxZoom: 5
      });
    //Add query protein
    cy.add(
      { data: { id: cyData[0].p1, 
                query: true,
                gene: cyData[0].p1_gene} }
    );
    //Add the top 10 primary interactors
    for (var i = 0; i < cyData.length; i++) {
      if (i < 10) {
        cy.add(
          { data: { id: cyData[i].p2,
                    gene: cyData[i].p2_gene } }
        );
      };
    //Add edges
      cy.add(
        { data: { id: i, 
          source: cyData[i].p1, 
          target: cyData[i].p2,
          exp: cyData[i].exp,
          type: cyData[i].type} }
      );
    };
    cy.layout({
      name: 'cose'
    });

    cy.on('select','node', selectedNodeHandler)
    cy.on('unselect','node', unselectedNodeHandler)
    cy.on('select','edge', selectededgeHandler)
    cy.on('unselect','edge', unselectededgeHandler)

  });

  // cyData[i].p1 + "--" + cyData[i].p2
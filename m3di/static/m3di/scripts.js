function populate_uniprot(){
    document.getElementById('input_uni').value="Q9BYF1";
    document.getElementById('input_var').value="199";
}

// 8

function convertJson(myId) {
  var cont = document.getElementById(myId).textContent
  return JSON.parse(cont.replaceAll('\\','').replace(/^"|"$/g, ''))
}

const cyEdges = convertJson('cyEdges');
const cyNodes = convertJson('cyNodes');

var selectedNodeHandler = function(evt) {
  $('#node').show();
  var node = evt.cyTarget.data();
  $("#node").html(`
  <p> Uniprot ID: ${node.id} </p>
  <p> Gene name: ${node.gene} </p>`);
}
var unselectedNodeHandler = function() {
  $('#node').hide();
}
var selectededgeHandler = function(evt) {
  $('#edge').show();
  var edge = evt.cyTarget.data();
  $("#edge").html(`
  <p> Interaction: ${edge.source} - ${edge.target} </p>
  <p> Experimental evidence score: ${edge.exp} </p>
  <p> Model/Structure: ${edge.type} </p>`);
}
var unselectededgeHandler = function() {
  $('#edge').hide();
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
    //Add nodes
    for (var i = 0; i < cyNodes.length; i++) {
        cy.add(
          { data: { id: cyNodes[i].uniprot,
                    idInt: i,
                    gene: cyNodes[i].gene } }
        );
      };
    //Add edges
    for (var i = 0; i < cyEdges.length; i++) {
      cy.add(
        { data: { id: cyEdges[i].p1 + '-' + cyEdges[i].p2, 
          source: cyEdges[i].p1, 
          target: cyEdges[i].p2,
          exp: cyEdges[i].exp,
          type: cyEdges[i].type} }
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



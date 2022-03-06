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

$('.node-operation').hide();
$('.edge-operation').hide();

var selectedNodeHandler = function(evt) {
  $('.node-operation').show();
  var node = evt.cyTarget.data();
  // $("#node").text("UniprotID: " + node_id);
  $("#node").html(`Uniprot ID: ${node.id}`);
}
var unselectedNodeHandler = function() {
  $('.node-operation').hide();
}
var selectededgeHandler = function(evt) {
  $('.edge-operation').show();
  var edge = evt.cyTarget.data();
  $("#edge").text("Interaction: " + edge.source + ' - ' + edge.target);
  $("#exp").text("Experimental evidence score: " + edge.exp);
  $("#type").text("Model/Structure: " + edge.type);
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



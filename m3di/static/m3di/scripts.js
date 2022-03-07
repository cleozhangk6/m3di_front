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
  <p> Uniprot ID: <a href="${node.link}">${node.id}</a></p>
  <p> Protein name: ${node.name} </p>
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
  <p> Experimental score: ${edge.exp} </p>
  <p> Model/Structure: ${edge.type} </p>
  <p> PDB: ${edge.pdb} </p>`);
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
          { data: { id: cyNodes[i].uniprot_id,
                    idInt: i,
                    link: cyNodes[i].protein_link,
                    name: cyNodes[i].protein_name,
                    gene: cyNodes[i].gene_name} }
        );
      };
    //Add edges
    for (var i = 0; i < cyEdges.length; i++) {
      cy.add(
        { data: { id: cyEdges[i].p1 + '-' + cyEdges[i].p2, 
          source: cyEdges[i].p1, 
          target: cyEdges[i].p2,
          exp: cyEdges[i].experimental,
          type: cyEdges[i].type,
          pdb: cyEdges[i].PDB_id} }
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



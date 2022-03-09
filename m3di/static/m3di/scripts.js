function populate_uniprot(){
    document.getElementById('input_uni').value="Q9BYF1";
    document.getElementById('input_var').value="199";
}

// 8

function convertJson(myId) {
  var cont = document.getElementById(myId).textContent
  return JSON.parse(cont.replace(/\\/g,'').replace(/^"|"$/g, ''))
}

const cyEdges = convertJson('cyEdges');
const cyNodes = convertJson('cyNodes');
// const cyEdges_raw = convertJson('cyEdges_raw');

var selectedNodeHandler = function(evt) {
  $('#node').show();
  var node = evt.cyTarget.data();
  $("#node").html(`
  <p> Protein name: <a href="${node.link}">${node.name}</a></p>
  <p> Uniprot ID: ${node.id} </p>
  <p> Gene name: ${node.gene} </p>
  <p> Organism: <i>Homo Sapiens</i> </p>`);
}
var unselectedNodeHandler = function() {
  $('#node').hide();
}
var selectedEdgeHandler = function(evt) {
  $('#edge').show();
  var edge = evt.cyTarget.data();
  if (edge.type != null) {
    $("#edge").html(`
    <p> Interaction: ${edge.source} - ${edge.target} </p>
    <p> Experimental score: ${edge.exp} </p>
    <p> Model/Structure: ${edge.type} </p>
    <p> PDB: <a href="https://www.rcsb.org/structure/${edge.pdb}">${edge.pdb}</a> </p>`);}
  else {
    $("#edge").html(`
    <p> Interaction: ${edge.source} - ${edge.target} </p>
    <p> Experimental score: ${edge.exp} </p>`)
  }
}
var unselectedEdgeHandler = function() {
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
      maxZoom: 2
      });
    //Add nodes
    for (var i = 0; i < cyNodes.length; i++) {
        cy.add(
          { data: { id: cyNodes[i].uniprot_id,
                    idInt: i,
                    link: cyNodes[i].protein_link,
                    name: cyNodes[i].protein_name,
                    gene: cyNodes[i].gene_name,
                    pos: cyNodes[i].pos} }
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
          pdb: cyEdges[i].PDB_id, 
          self: cyEdges[i].self} }
      );
    };
    cy.layout({
      name: 'cose'
    });

  
    cy.on('select','node', selectedNodeHandler)
    cy.on('unselect','node', unselectedNodeHandler)
    cy.on('select','edge', selectedEdgeHandler)
    cy.on('unselect','edge', unselectedEdgeHandler)

    // cy.on('mouseover','node', function(event) {
    //   var node = event.cyTarget;
    //   node.qtip({
    //     content: 'hello',
    //     show: {
    //       event: event.type,
    //       ready: true
    //    },
    //    hide: {
    //       event: 'mouseout unfocus'
    //    }
    //   },event)
    // })

    // cy.on('mouseover','node', selectedNodeHandler)
    // cy.on('mouseout','node', unselectedNodeHandler)
    // cy.on('mouseover','edge', selectededgeHandler)
    // cy.on('mouseout','edge', unselectededgeHandler)

  });

// Display self-interaction checkbox
function displaySelf() {
  checkSelf = document.getElementById("check_self");
  if (checkSelf.checked == true) {
    cy.edges('[?self]').style({'opacity':'1'});
  } else {
    cy.edges('[?self]').style({'opacity':'0'});
  }
  
}

//cy.nodes('[id=\"P05556\"]').addClass(query

// cy.nodes('[id=\"P05556\"]').style({'background-color':'blue'})
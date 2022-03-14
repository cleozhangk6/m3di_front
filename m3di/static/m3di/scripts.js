function populateInput(uniprot,variant){
    document.getElementById('input_uni').value=uniprot;
    document.getElementById('input_var').value=variant;
}

function toggleAdvance(){
  var el = document.getElementsByClassName('advanced-settings');
  var txt = document.getElementById('toggle-advance');
  for (var i = 0; i < el.length; i++) {
    if (el[i].style.display === "none") {
      el[i].style.display = "table-row";
      txt.textContent = 'Hide advanced';
    } else {
      el[i].style.display = "none";
      txt.textContent = 'Show advanced';
    }
  }
}

function showCustom(select,input){
  var sel = document.getElementById(select);
  var cus = document.getElementById(input);
  if (sel.value === 'Custom') {
    cus.style.visibility = 'visible';
  } else {
    cus.style.visibility = 'hidden';
  }
}

// Cytoscape

function convertJson(myId) {
  var cont = document.getElementById(myId).textContent
  return JSON.parse(cont.replace(/\\/g,'').replace(/^"|"$/g, ''))
}

var selectedNodeHandler = function(evt) {
  $('#node').show();
  var node = evt.cyTarget.data();
  $("#node").html(`
  <p> Protein: <a href="${node.link}">${node.name}</a></p>
  <p> Uniprot ID: ${node.id} </p>
  <p> Gene ID: ${node.gene} </p>
  <p> Organism: <i>Homo Sapiens</i> </p>
  <p> Residues interacting: ${node.pos}</p>`);
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

function executeCy() {
  Promise.all([
    fetch('/static/m3di/cy-style.json')
    .then(function(res) {
      return res.json()
    })
  ])
    .then(function(dataArray) {
      const cyEdges = convertJson('cyEdges');
      const cyNodes = convertJson('cyNodes');
      const query_uni = document.getElementById('query_uni').textContent;
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
      //Select and enlarge query protein node
      cy.nodes('[id="' + query_uni + '"]').style({"width": "60px","height": "60px", "shape": "square"})
      //Add event listeners when selecting node/edges
      cy.on('select','node', selectedNodeHandler)
      cy.on('unselect','node', unselectedNodeHandler)
      cy.on('select','edge', selectedEdgeHandler)
      cy.on('unselect','edge', unselectedEdgeHandler)
  
    });
};


//Display self-interaction checkbox
function displaySelf() {
  checkSelf = document.getElementById("check_self");
  if (checkSelf.checked == true) {
    cy.edges('[?self]').style({'opacity':'1'});
  } else {
    cy.edges('[?self]').style({'opacity':'0'});
  }  
}

//Color proteins involved in interface
function colorPos() {
  checkPos = document.getElementById("check_pos");
  if (checkPos.checked == true) {
    cy.nodes('[?pos]').style({'background-color':'#d96226',"text-outline-color": "#d96226"});
  } else {
    cy.nodes('[?pos]').style({'background-color':'#605C69',"text-outline-color": "#605C69"});
  }  
}



//cc0000, FD333
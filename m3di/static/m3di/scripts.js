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
      txt.textContent = 'Hide Advanced';
    } else {
      el[i].style.display = "none";
      txt.textContent = 'Show Advanced';
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

var selectedNodeHandler = function(evt) {
  $('#node').show();
  var node = evt.cyTarget.data();
  if (document.getElementById('query_var') != null && node.pos != null) {
    const query_uni = document.getElementById('query_uni').textContent;
    const query_var = document.getElementById('query_var').textContent;
    $("#node").html(`
    <p> <b>Protein:</b> ${node.name}
      <a target="_blank" href="${node.link}">(link to UniProt)</a></p>
    <p> <b>UniProt ID:</b> ${node.id}
      <a onclick="populateInput('${node.id}','')">(fill search)</a></p>
    <p> <b>Gene ID:</b> ${node.gene} </p>
    <p> <b>Organism:</b> <i>Homo Sapiens</i> </p>
    <p> <b>Residues involved in the interaction surface with 
        residue ${query_var} of ${query_uni}:</b> 
        ${node.pos}</p> </br>`);
  } else {
    $("#node").html(`
    <p> <b>Protein:</b> ${node.name}
      <a target="_blank" href="${node.link}">(link to UniProt)</a></p>
    <p> <b>UniProt ID:</b> ${node.id}
      <a onclick="populateInput('${node.id}','')">(fill search)</a></p>
    <p> <b>Gene ID:</b> ${node.gene} </p>
    <p> <b>Organism:</b> <i>Homo Sapiens</i> </p> </br>`);
  }
}
var unselectedNodeHandler = function() {
  $('#node').hide();
}
var selectedEdgeHandler = function(evt) {
  $('#edge').show();
  var edge = evt.cyTarget.data();
  if (edge.type != null && edge.self == null) {
    $("#edge").html(`
    <p> <b>Interaction:</b> ${edge.source} - ${edge.target} </p>
    <p> <b>Experimental score:</b> ${edge.exp} </p>
    <p> <b>Structure or Model:</b> ${edge.type} </p>
    <p> <b>PDB (or model template) ID:</b> ${edge.pdb} 
      <a target="_blank" href="https://www.rcsb.org/structure/${edge.pdb}">
      (link to PDB) </a></p> </br>`);
  } else if (edge.self != null) {
    $("#edge").html(`
    <p> <b>Interaction:</b> Self-interaction </p>
    <p> <b>Model or Structure:</b> ${edge.type} </p>
    <p> <b>PDB (or model template) ID:</b> ${edge.pdb} 
      <a target="_blank" href="https://www.rcsb.org/structure/${edge.pdb}">
      (link to PDB) </a></p> </br>`);
  } else {
    $("#edge").html(`
    <p> <b>Interaction:</b> ${edge.source} - ${edge.target} </p>
    <p> <b>Experimental score:</b> ${edge.exp} </p> </br>`)
  }
}
var unselectedEdgeHandler = function() {
  $('#edge').hide();
}

function convertJson(myId) {
  var cont = document.getElementById(myId).textContent
  return JSON.parse(cont.replace(/\\|^"|"$/g, ''))
  //Regex: remove backward slashes and boundary quotationmarks
}

function executeCy() {
  const cyEdges = convertJson('cyEdges');
  const cyNodes = convertJson('cyNodes');
  const query_uni = document.getElementById('query_uni').textContent;
  const query_sco = Number(document.getElementById('query_sco').textContent)*1000;
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
      //Filter out edges under threshold
      cy.edges('[exp<"' + query_sco + '"]').style({"opacity":0})
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
    cy.nodes('[?pos]').style({'background-color':'#A6CA6E',"text-outline-color": "#A6CA6E"});
  } else {
    cy.nodes('[?pos]').style({'background-color':'#605C69',"text-outline-color": "#605C69"});
  }  
}



//cc0000, FD333
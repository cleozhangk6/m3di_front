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
  }
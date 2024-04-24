// When the user clicks on <div>, open the popup

function quickSwap() {
  const popup = document.getElementById("swaps");
  popup.classList.toggle("show");
}
function Popup() {
  const popup = document.getElementById("pop");
  popup.classList.toggle("show");

  const group_background = document.getElementById("group_background");
  group_background.classList.toggle("blur");
}

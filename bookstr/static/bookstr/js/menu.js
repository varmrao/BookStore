/*
$(function(){
    var $select = $(".1-10");
    for (i=1;i<=10;i++){
        $select.append($('<option></option>').val(i).html(i))
    }
}); */

var dropdown = document.getElementById("dropdown");

var list = document.getElementById("noc");
//list.setAttribute("id","noc");
//dropdown.appendChild(list);

for (var i =1;i<=10;i++) {
  var option = document.createElement("option");
  option.setAttribute("value", String(i));
  option.text = String(i);
  list.appendChild(option);
}


import {set_loader} from "./loader.js";
import {search_paper} from "./search_paper.js";
export let valueSearch;
 export function initialize_autocomplete (dict_authors_titles){
 $(document).ready(function(){
    $('input.autocomplete').autocomplete({
      data: dict_authors_titles,
      limit: 4,
       onAutocomplete: function(val) {
        valueSearch = $("#autocomplete-input").val();
        set_loader();
        setTimeout(function(){ search_paper(); }, 1500);
    },
    minLength: 3,
    });
  });
 }

$("#autocomplete-input").keyup(function(event){
    if(event.keyCode ==13){
        valueSearch = $("#autocomplete-input").val();
        set_loader();
        setTimeout(function(){ search_paper(); }, 1500);


    }
});



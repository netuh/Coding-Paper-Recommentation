
import {search_paper_characteristic} from "./search_paper_characteristic_service.js";
import {set_loader} from "./loader.js";
export let searchCharacteristicForm

export function init_search_characteristics() {
  $("#search").click(function () {
    searchCharacteristicForm = {};
    searchCharacteristicForm.design = $("#design").val();
    searchCharacteristicForm.task = $("#task").formSelect('getSelectedValues');
    searchCharacteristicForm.measurement = $("#measurement").formSelect('getSelectedValues');
    searchCharacteristicForm.sample = $("#sample").val();
    set_loader();
    setTimeout(function(){ search_paper_characteristic() }, 1500);








  });
}
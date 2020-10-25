import {mount_pagination, mount_results} from "./mount_pagination.js";
import {searchCharacteristicForm} from "./init_event_search_characteristics.js";

async function search_paper_characteristic(url=`${window.location.origin}/search_characteristics_teste`){
    const result = await fetch(url,{
        method: "POST",
        body:JSON.stringify(searchCharacteristicForm),
        credentials: "include",
        cache: "no-cache",
        headers: new Headers({
            "content-type":"application/json"
        })
    })

    const date = await result.json();
    mount_results(date);

    if(date.papers.length > 0)
        mount_pagination(date,`${window.location.origin}/search_characteristics_teste`)

    $("html, body").animate({ scrollTop: "0" });

}

$("#result-search").on("click","li.element-list a", function(event){
    let url=this.href;
    event.preventDefault();
    const urlParamPage = parseInt(new URLSearchParams(url).get('page'));
    searchCharacteristicForm.page = urlParamPage
    search_paper_characteristic(url);

});

export {search_paper_characteristic}
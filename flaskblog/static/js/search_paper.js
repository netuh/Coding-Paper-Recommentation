
import {mount_results, mount_pagination} from "./mount_pagination.js";
import {valueSearch} from "./init_autocomplete.js";

async function search_paper(url=`${window.location.origin}/search?search=${valueSearch}`){
    const result = await fetch(url,{
        method: "GET",
        credentials: "include",
        cache: "no-cache",
        headers: new Headers({
            "content-type":"application/json"
        })
    })

    const date = await result.json();
    mount_results(date);

    if(date.papers.length > 0)
        mount_pagination(date,`${window.location.origin}/search`)

     $("html, body").animate({ scrollTop: "0" });

}

$("#result-search").on("click","li.element-list a", function(event){
    let url=this.href;
    url += `&${valueSearch}`;
    event.preventDefault();
    search_paper(url);

});

export {search_paper}
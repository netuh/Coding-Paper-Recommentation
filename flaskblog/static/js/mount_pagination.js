
export function mount_results(date){
    let publications = "";
    for (let publication of date.papers){
    publications +=
        `<div class="row">
            <div class="col s12 m6">
                <div class="card">
                    <div class="card-content deep-purple-text text-lighten-1">
                        <span class="card-title">${publication.name}</span>
                            <p>${publication.authors}</p>
                    </div>
                    <div class="card-action">
                        <a href="${window.location.origin}/details/${publication.id}">More Info...</a>
                    </div>
                 </div>
            </div>
        </div>`


    }
    $("#result-search").html(publications);
}






export function mount_pagination(date, url){
        let pagination="";
    pagination+=`<ul class="pagination">`

    if(date.page_conf.has_prev)
        pagination+=`<li class="waves-effect element-list"><a href="${url}?page=${date.page_conf.prev_num}"><i class="material-icons">chevron_left</i></a></li>`
    else
         pagination+=`<li class="disabled"><a><i class="material-icons">chevron_left</i></a></li>`

    for(let page of date.page_conf.pages){
        if(page) {
            if(page==date.page_conf.page)
                pagination+=`<li class="active element-list"><a href="${url}?page=${page}">${page}</a></li>`
            else
                pagination+=`<li class="waves-effect element-list"><a href="${url}?page=${page}">${page}</a></li>`
        }
        else{
            pagination+=`<li>...</li>`
        }
    }

    if(date.page_conf.has_next)
        pagination+=`<li class="waves-effect element-list"><a href="${url}?page=${date.page_conf.next_num}"><i class="material-icons">chevron_right</i></a></li>`
    else
         pagination+=`<li class="disabled"><a><i class="material-icons">chevron_right</i></a></li>`


    $("#result-search").append(pagination);

}



function initialize_autocomplete (dict_authors_titles){
 $(document).ready(function(){
    $('input.autocomplete').autocomplete({
      data: dict_authors_titles,
      limit: 4,
       onAutocomplete: function(val) {
        set_loader();
    },
    minLength: 3,
    });
  });
 }

$("#autocomplete-input").keyup(function(event){
    if(event.keyCode ==13){
      set_loader();


    }
});


function set_loader(){
    $("#result-search").html(
        ` <div class="progress">
            <div class="indeterminate">
            </div>
          </div>`
          )
    setTimeout(function(){ search_paper(); }, 1500);

}


async function search_paper(url=`${window.location.origin}/search_teste?search=${$("#autocomplete-input").val()}`){
    const result = await fetch(url,{
        method: "GET",
        credentials: "include",
        cache: "no-cache",
        headers: new Headers({
            "content-type":"application/json"
        })
    })

    const date = await result.json();
    search_results(date);
    if(date.papers.length > 0)
        mount_pagination(date)

}

function search_results(date){
    let publications = "";
    for (publication of date.papers){
    publications +=
        `<div class="row">
            <div class="col s12 m6">
                <div class="card">
                    <div class="card-content deep-purple-text text-lighten-1">
                        <span class="card-title">${publication.name}</span>
                            <p>${publication.authors}</p>
                    </div>
                    <div class="card-action">
                        <a href="${window.location.origin}/details_teste/${publication.id}">More Info...</a>
                    </div>
                 </div>
            </div>
        </div>`


    }
    $("#result-search").html(publications);
}

function mount_pagination(date){
    let pagination="";
    pagination+=`<ul class="pagination">`

    if(date.page_conf.has_prev)
        pagination+=`<li class="waves-effect element-list"><a href="${window.location.origin}/search_teste?search=${date.search}&page=${date.page_conf.prev_num}"><i class="material-icons">chevron_left</i></a></li>`
    else
         pagination+=`<li class="disabled"><a><i class="material-icons">chevron_left</i></a></li>`

    for(page of date.page_conf.pages){
        if(page) {
            if(page==date.page_conf.page)
                pagination+=`<li class="active element-list"><a href="${window.location.origin}/search_teste?search=${date.search}&page=${page}">${page}</a></li>`
            else
                pagination+=`<li class="waves-effect element-list"><a href="${window.location.origin}/search_teste?search=${date.search}&page=${page}">${page}</a></li>`
        }
        else{
            pagination+=`<li>...</li>`
        }
    }

    if(date.page_conf.has_next)
        pagination+=`<li class="waves-effect element-list"><a href="${window.location.origin}/search_teste?search=${date.search}&page=${date.page_conf.next_num}"><i class="material-icons">chevron_right</i></a></li>`
    else
         pagination+=`<li class="disabled"><a><i class="material-icons">chevron_right</i></a></li>`


    $("#result-search").append(pagination);

}

$("#result-search").on("click","li.element-list", function(event){
    let url=event.target.href;
    event.preventDefault();
    if(!url)
        url=event.target.parentNode.href;

    search_paper(url);
    window.scrollTo(0,0);

});


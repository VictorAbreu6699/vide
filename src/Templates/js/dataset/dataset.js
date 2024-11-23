$(document).ready(function(){
    user_logged = checkUserLogin()

    if(user_logged){
        $("#create-database-card").show()
    }
    // Ao abrir a pagina carrega os cards
    createDatabaseCards()
})
$("#search-input-datasets").on("input", (e) => createDatabaseCards())

function createDatabaseCards() {
    $('#row-datasets').children().not('#create-database-card').remove();
    result = request("GET", "/datasets/get-datasets?" + $("#form-input-datasets").serialize())
    if(result.status != 201)
        return;

    data = result.data.data
    data.forEach(function(dataset) {
        hmtl = `<div class="col-3 mb-4">
                    <div class="card" style="width: 18rem; background-color: #1E1E2E;">
                      <div class="card-body text-center" style="color: white">
                          <div class="card-title">${dataset.name}</div>
                          <div class="text-center card-text">
                              <i style="font-size: 150px; color: white" class="fa fa-database" aria-hidden="true"></i>
                              </br>
                              <div class="dataset-title mt-2">Criado por <i data-bs-toggle="tooltip" data-bs-placement="top" title="${dataset.user_email}">${dataset.user_name}</i></div>
                              <a href="/cadastro-dataset" style="background-color: #4E598D; color: white" class="btn mt-3" target="_blank">
                                  Visualizar
                              </a>
                          </div>
                      </div>
                    </div>
                </div>`
        $("#row-datasets").append(hmtl);
    });
}

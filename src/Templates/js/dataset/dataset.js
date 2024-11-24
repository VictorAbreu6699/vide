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
                              <button dataset-id="${dataset.id}" type="button" style="background-color: #4E598D; color: white" class="btn mt-3 btn-visualization-modal">
                                  Visualizar
                              </button>
                          </div>
                      </div>
                    </div>
                </div>`
        $("#row-datasets").append(hmtl);
    });
    $(".btn-visualization-modal").off("click")
    $(".btn-visualization-modal").on("click", function(e) {
        dataset_id = $(this).attr("dataset-id");
        fillModalDataset(dataset_id)
    })
}

function fillModalDataset(dataset_id){
    result = request("GET", "/datasets/show-dataset/"+dataset_id)
    if(result.status != 201)
        return;

    data = result.data.data
    $("#dataset-show-modal-label").text(data.name)
    $("#dataset-show-modal-description").text(data.description)
    $("#dataset-show-modal-download").attr("download", data.name + data.extension)
    $("#dataset-show-modal-download").attr("href", "/datasets/download-file/" + data.id)

    let dataset_modal = new bootstrap.Modal(document.getElementById('dataset-show-modal'), {
      keyboard: false
    })

    dataset_modal.show()
}


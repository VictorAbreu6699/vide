$(document).ready(function(){
    user_logged = checkUserLogin()

    if(user_logged){
        $("#create-database-card").show()
    }
    // Ao abrir a pagina carrega os cards
    createDatabaseCards()
    openModelOnLoadPage()
    // Inicializar o tooltip do Bootstrap
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
})
$("#search-input-datasets").on("input", (e) => createDatabaseCards())

$("#dataset-show-modal").on("hide.bs.modal", (e) => removeURLParam("dataset_id"))

$("#button-share-link").on("click", copyUrl)

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
        removeURLParam("dataset_id")
        fillModalDataset(dataset_id)
        setUrlParam({key: "dataset_id", value: dataset_id})
    })
}

function fillModalDataset(dataset_id){
    result = request("GET", "/datasets/show-dataset/"+dataset_id)
    if(result.status != 201)
        return;

    data = result.data.data
    $("#dataset-show-modal-label").text(data.name)
    $("#dataset-show-modal-description").text(data.description)
    created_at = moment(data.created_at, "YYYY-MM-DD HH:mm:ss").format('DD/MM/YYYY HH:mm:ss')
    $("#dataset-show-modal-created-at").text(created_at)
    $("#dataset-show-modal-download").attr("download", data.name + data.extension)
    $("#dataset-show-modal-download").attr("href", "/datasets/download-file/" + data.id)

    let dataset_modal = new bootstrap.Modal(document.getElementById('dataset-show-modal'), {
      keyboard: false
    })

    dataset_modal.show()
}

function openModelOnLoadPage(){
    let params = new URLSearchParams(window.location.search);
    let valueParam = params.get("dataset_id");
    // Caso o usuário preencha o parametro, exibe a base de dados
    if(valueParam)
        fillModalDataset(valueParam)
}

function copyUrl() {
    let currentUrl = new URL(window.location.href);

     // Usar a API Clipboard para copiar o texto
    navigator.clipboard.writeText(currentUrl);

    // Alterar o texto do tooltip para "Copiado!"
    const tooltip = bootstrap.Tooltip.getInstance(this); // Obter a instância do tooltip
    tooltip.setContent({ '.tooltip-inner': 'Copiado!' });

    // Mostrar o tooltip e redefinir após 2 segundos
    $(this).tooltip("show");
    setTimeout(() => {
        $(this).tooltip("hide");
        tooltip.setContent({ '.tooltip-inner': 'Copiar Link' });
    }, 2000);
}



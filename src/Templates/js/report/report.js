$(document).ready(function(){
    user_logged = checkUserLogin()

    if(user_logged){
        $("#create-report-card").show()
    }
    // Ao abrir a pagina carrega os cards
    createReportCards()
    openModelOnLoadPage()
    // Inicializar o tooltip do Bootstrap
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
})
$("#search-input-reports").on("input", (e) => createReportCards())

$("#report-show-modal").on("hide.bs.modal", (e) => removeURLParam("report_id"))

function createReportCards() {
    $('#row-reports').children().not('#create-report-card').remove();
    result = request("GET", "/reports/get-reports?" + $("#form-input-reports").serialize())
    if(result.status != 201)
        return;

    data = result.data.data
    data.forEach(function(report) {
        hmtl = `<div class="col-3 mb-4">
                    <div class="card card-reports">
                      <div class="card-body text-center" style="color: white">
                          <div class="card-title">${report.name}</div>
                          <div class="text-center card-text">
                              <i style="font-size: 150px; color: white" class="fa fa-bar-chart" aria-hidden="true"></i>
                              </br>
                              <div class="report-title mt-2">Criado por <i data-bs-toggle="tooltip" data-bs-placement="top" title="${report.user_email}">${report.user_name}</i></div>
                              <button report-id="${report.id}" type="button" style="background-color: #4E598D; color: white" class="btn mt-3 btn-visualization-modal">
                                  Visualizar
                              </button>
                          </div>
                      </div>
                    </div>
                </div>`
        $("#row-reports").append(hmtl);
    });
    $(".btn-visualization-modal").off("click")
    $(".btn-visualization-modal").on("click", function(e) {
        report_id = $(this).attr("report-id");
        removeURLParam("report_id")
        fillModalReport(report_id)
        setUrlParam({key: "report_id", value: report_id})
    })
}

function fillModalReport(report_id){
    result = request("GET", "/reports/show-report/"+report_id)
    if(result.status != 201)
        return;

    data = result.data.data
    $("#report-show-modal-label").text(data.name)
    $("#report-show-modal-description").text(data.description)
    created_at = moment(data.created_at, "YYYY-MM-DD HH:mm:ss").format('DD/MM/YYYY HH:mm:ss')
    updated_at = moment(data.updated_at, "YYYY-MM-DD HH:mm:ss").format('DD/MM/YYYY HH:mm:ss')
    $("#report-show-modal-created-at").text(created_at)
    $("#report-show-modal-updated-at").text(updated_at)
    $("#report-show-modal-download").attr("download", data.name + data.extension)
    $("#report-show-modal-download").attr("href", "/reports/download-file/" + data.id)
    $("#button-access-link").attr("href", "/relatorios/" + data.id)
    $("#button-access-edit-link").attr("href", "/editar-relatorio/" + data.id)
    user_id = data.user_id
    user_is_logged = checkUserLogin()

    if(user_is_logged){
        user_logged_request = request("GET", "/auth/show-logged-user")
        if(user_logged_request.status == 200 && user_logged_request.data.data.id == user_id)
        {
            $("#button-access-edit-link").show()
        }
        else{
            $("#button-access-edit-link").hide()
        }

    }
    else{
        $("#button-access-edit-link").hide()
    }

    let report_modal = new bootstrap.Modal(document.getElementById('report-show-modal'), {
      keyboard: false
    })

    report_modal.show()
}

function openModelOnLoadPage(){
    let params = new URLSearchParams(window.location.search);
    let valueParam = params.get("report_id");
    // Caso o usuário preencha o parametro, exibe a base de dados
    if(valueParam)
        fillModalReport(valueParam)
}



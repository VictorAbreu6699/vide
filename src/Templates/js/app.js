$(document).ready(function(){
    setSidebarActiveMenu()
    changeSidebarAfterLogin()
    $("#sidebar-logout-button-link").on("click", () => logout())
})

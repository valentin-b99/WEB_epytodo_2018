$(document).ready(function () {
    $(".datepicker-begin-i").datepicker({
        format: 'yyyy/mm/dd',
        startDate: '0d'
    });
    $(".clockpicker-begin-i").clockpicker({
        autoclose: true,
        'default': 'now'
    });
    $(".datepicker-end-i").datepicker({
        format: 'yyyy/mm/dd',
        startDate: '0d'
    });
    $(".clockpicker-end-i").clockpicker({
        autoclose: true,
        'default': 'now'
    });
    $(".datepicker-begin-i").on("changeDate", function (e) {
        $("#datepicker-end-i").datepicker("setStartDate", e.date);
        $("#datepicker-end").val("");
    });
    $(".private-status").on("click", function() {
        if ($(this).is(":checked")) {
            $(this).parent().find("span").addClass("badge-danger");
            $(this).parent().find("span").removeClass("badge-success");
            $(this).parent().find("span").text("Private");
        } else {
            $(this).parent().find("span").removeClass("badge-danger");
            $(this).parent().find("span").addClass("badge-success");
            $(this).parent().find("span").text("Public");
        }
    });
});
(function ($) {
  "use strict";

  $(window).on("load", function () {
    $(".preloader").delay(200).fadeOut("slow");
  });
})(jQuery);


$(document).ready(function () {
  $("#stock-btn").click(function (e) {
    e.preventDefault();
    var stock = $("#stock-name").val();
    var from_date = $("#from_date").val();
    var to_date = $("#to_date").val();

    $.ajax({
      url: "/getStockData",
      type: "post",
      data: { stock: stock, from_date: from_date, to_date: to_date },
      beforeSend: function () {
        $("#loader").show();
        $("#stock-data").hide();
      },
      success: function (response) {
        $(".stock-response").empty();
        $(".stock-response").append(response.htmlresponse);
      },
      complete: function (data) {
        $("#loader").hide();
        $("#stock-data").show();
        $(".background-image").hide();
      },
    });
  });
});

$(document).ready(function () {
  $("#model-btn").click(function (e) {
    var stock = $("#model-stock").val();
    e.preventDefault();
    $.ajax({
      url: "/predict",
      type: "post",
      data: { stock: stock },
      beforeSend: function () {
        $("#loader").show();
        $("#sentiment").hide();
      },
      success: function (response) {
        $(".model-response").empty();
        $(".model-response").append(response.htmlresponse);
      },
      complete: function (data) {
        $("#loader").hide();
        $("#sentiment").show();
        $(".background-image").hide();
      },
    });
  });
});

$("form[name=register-form]").submit(function (e) {
  e.preventDefault();
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,

    success: function (resp) {
      window.location.href = "/data";
    },
    error: function (resp) {
      $error.text(resp.responseJSON.error).removeClass("error-hidden");
    },
  });
});

$("form[name=login-form]").submit(function (e) {
  e.preventDefault();
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,

    success: function (resp) {
      window.location.href = "/data";
    },
    error: function (resp) {
      $error.text(resp.responseJSON.error).removeClass("error-hidden");
    },
  });
});

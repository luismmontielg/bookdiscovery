function createAutoClosingAlert(selector, delay) {
   var alert = $(selector).alert();
   window.setTimeout(function() { alert.fadeOut() }, delay);
}

function alertN(text, selector){ 
    $(selector).text(text);
    $(selector).fadeIn();
    createAutoClosingAlert(selector, 1800);
}

function wantToReadSuccess(e) {
    return function (data) {
        e.contents().last()[0].textContent = " Remove from list";
        e.attr("class", "btn btn-danger remove-from-list-btn");
        $(e.children()[0]).attr("class", "icon-remove-sign");
        alertN("The book was added to your 'to-read' list", "#ok-div");
    }
}

function failedToAddBook(e) {
    return function(data) {
        alertN("Failed to add book", "#error-div")
    }
}

function failedToRemoveBook(data) {
    alertN("Failed to remove book from list", "#error-div")
}

function wantToReadClicked(ele) {
    var e = $(ele.target);
    var book_id = e.attr("bid");
    $.post('/book/'+ book_id + "/add_relation/", {
        "read": 0
    }).done(wantToReadSuccess(e)).fail(failedToAddBook(e));
}

function alreadyReadSuccess(e) {
    return function (data) {
        e.prev().remove();
        e.contents().last()[0].textContent = " Remove from list";
        e.attr("class", "btn btn-danger remove-from-list-btn");
        $(e.children()[0]).attr("class", "icon-remove-sign");
        alertN("The book was added to your 'read' list", "#ok-div");
    }
}

function alreadyReadFailed(e){
    return function (data){
        alertN("Failed to add book", "#error-div")
    }
}

function alreadyReadClicked (ele) {
    var e = $(ele.target);
    var book_id = e.attr("bid");
    $.post('/book/'+ book_id + "/add_relation/", {
        "read": 1
    }).done(alreadyReadSuccess(e)).fail(alreadyReadFailed(e));
}

function removeFromListFailed(e) {
    return function(data){
        $("#error-div").text("Failed to remove book");
        $("#error-div").fadeIn();
        createAutoClosingAlert("#error-div", 1800);
    }
}

function removeFromListSuccess(e, book_id) {
    return function (data){
        var nextText = e.next().contents().last()[0].textContent;
        // removed from 'want-to-read' list
        var already = " already read";
        if (nextText.toLowerCase().trim() == already.toLowerCase().trim()) {
            e.contents().last()[0].textContent = " Want to read";
            $(e.children()[0]).attr("class", "icon-bookmark");
            e.attr("class", "btn btn-primary want-to-read-btn");
        } else {
            e.contents().last()[0].textContent = " Already read";
            e.attr("class", "btn already-read-btn");
            $(e.children()[0]).attr("class", "icon-check");
            var str = '<div bid="'+ book_id + '" class="btn btn-primary want-to-read-btn"><i class="icon-bookmark"></i>&nbsp;Want to read</div>';
            $(str).insertBefore(e);
        }
        alertN("The book was removed from the list", "#ok-div");
    }
}
function removeFromListClicked (ele) {
        var e = $(ele.target);
        var book_id = e.attr("bid");
        $.post('/book/'+ book_id + "/add_relation/", {
            "read": -1,
        }).done(removeFromListSuccess(e, book_id)).fail(removeFromListFailed(e));
    }

$(document).ready(function() {
    $().alert();
    $(".already-read-btn").live("click", alreadyReadClicked);
    $(".want-to-read-btn").live("click", wantToReadClicked);
    $(".remove-from-list-btn").live("click", removeFromListClicked);
});

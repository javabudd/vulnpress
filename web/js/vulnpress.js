$(document).ready(function() {
    $('#exploit-form').on('submit', function(e) {
        e.preventDefault();
        var found = $('.found'),
            not_found = $('.not-found'),
            error = $('#error');
        found.empty();
        not_found.empty();
        error.empty().addClass('hidden');
        $.ajax({
            url: '/',
            dataType: 'json',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.error) {
                    $('#error').html(response.error).removeClass('hidden');
                } else {
                    $.each(response.found, function(exploit_id, exploit) {
                         found.append('<li><a target="_blank" href="' + exploit.exploiturl + '">' + exploit.name + '</a></li>');
                    });
                    $.each(response.not_found, function(exploit_id, exploit) {
                         not_found.append('<li><a target="_blank" href="' + exploit.exploiturl + '">' + exploit.name + '</a></li>');
                    });
                }
            }
        });
    });

    var $button = $("<div id='source-button' class='btn btn-primary btn-xs'>&lt; &gt;</div>").click(function(){
        var html = $(this).parent().html();
        html = cleanSource(html);
        $("#source-modal pre").text(html);
        $("#source-modal").modal();
    });

    $('.bs-component [data-toggle="popover"]').popover();
    $('.bs-component [data-toggle="tooltip"]').tooltip();

    $(".bs-component").hover(function(){
        $(this).append($button);
        $button.show();
    }, function(){
        $button.hide();
    });

    function cleanSource(html) {
    var lines = html.split(/\n/);

    lines.shift();
    lines.splice(-1, 1);

    var indentSize = lines[0].length - lines[0].trim().length,
        re = new RegExp(" {" + indentSize + "}");

    lines = lines.map(function(line){
        if (line.match(re)) {
            line = line.substring(indentSize);
        }

      return line;
    });

    lines = lines.join("\n");

    return lines;
  }
});

$body = $("body");
$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
    ajaxStop: function() { $body.removeClass("loading"); }
});

$(window).scroll(function () {
    var top = $(document).scrollTop();
    $('.splash').css({
        'background-position': '0px -'+(top/3).toFixed(2)+'px'
    });
    if (top > 50) {
         $('#home > .navbar').removeClass('navbar-transparent');
    }
    else {
         $('#home > .navbar').addClass('navbar-transparent');
    }
});
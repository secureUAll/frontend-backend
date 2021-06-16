$(document).ready(() => {

    // Initialize helpers
    // (all elements with attrs data-content, data-helper and title)
    const helpers = {};

    $("[data-helper][title][data-content]").each((i, element) => {
        let action = '';
        if (i!=0) {
            action += '<p class="btn btn-sm btn-outline-primary mb-0 mr-auto previousHelper">Previous</p>';
        }
        if ($("[data-helper][title][data-content]").length==i+1) {
            action += '<p class="btn btn-sm btn-primary mb-0 ml-auto finishHelper">Finish</p>';
        }
        action += ($("[data-helper][title][data-content]").length>i+1) ? '<p class="btn btn-sm btn-primary mb-0 ml-auto nextHelper">Next</p>' : '';
        var popover = new bootstrap.Popover(element, {
            'trigger': 'manual',
            'html': true,
            'template': `<div class="popover" role="tooltip"><div class="arrow"></div><h6 class="popover-header mt-0 bg-white"></h6><div class="popover-body p-2"></div><div class="d-flex flex-row flex-wrap pl-2 pr-2 pb-2">${action}</div></div>`
        });
        helpers[$(element).data('helper')] = popover;
    });

    // If there are helpers available, show help btn
    if (Object.keys(helpers).length>0) {
        $("#help").removeClass("d-none");
    }

    // When click on help btn, show first
    let index = 0;
    let firstTime = true;
    $("#help").click(() => {
        // Hide current
        helpers[Object.keys(helpers)[index]].hide();
        // Set index to 0
        index = 0;
        // Show 0
        showHelper();
    });

    // Handlers
    const nextHelper = () => {
        // Hide current
        helpers[Object.keys(helpers)[index]].hide();
        // Update index
        index = index+1>=Object.keys(helpers).length ? 0 : index+1;
        // Show next
        showHelper();
    }

    const prevHelper = () => {
        // Hide current
        helpers[Object.keys(helpers)[index]].hide();
        // Update index
        index = index-1<0 ? Object.keys(helpers).length-1 : index-1;
        // Show next
        showHelper();
    }

    const finishHelper = () => {
        // Hide current
        helpers[Object.keys(helpers)[index]].hide();
    }

    const showHelper = () => {
        // Show helper for current index
        helpers[Object.keys(helpers)[index]].show();
        // Create handlers for .nextHelper click
        $(".nextHelper").unbind('click').click(() => nextHelper());
        $(".finishHelper").unbind('click').click(() => finishHelper());
        $(".previousHelper").unbind('click').click(() => prevHelper());
    }
});
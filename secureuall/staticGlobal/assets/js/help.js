/**

    This script is used to create help interfaces for to help users.

    To use it, just create a button with id="help". Example below:
        <button class="btn btn-outline-primary d-none" id="help"><i class="now-ui-icons travel_info"></i> Ajuda</button>

    Then, on elements that you want to provide help define the following attributes:
        data-helper="0"  // Help order (can't have more than one with same order!)
        data-placement="top" // This is optional. Available options are: left, right, top, bottom
        title="Your personal data" // The help title
        data-content="In this section you can see your personal data. You can not edit it, as it is provided by UA IdP." // The help text

    This attributes can be defined in any HTML element. Below are some examples.
        <h6
            class="mt-5"
            data-helper="0"
            data-placement="top"
            title="Your personal data"
            data-content="In this section you can see your personal data. You can not edit it, as it is provided by UA IdP."
        >Personal information</h6>
        <th
            data-helper="2"
            data-placement="right"
            title="Email"
            data-content="This is the method activated by default."
        >
            Email
        </th>

*/
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
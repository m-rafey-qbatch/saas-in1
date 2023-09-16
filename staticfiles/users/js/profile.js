
$(document).ready(function() {
    // Mobile
    var mobileValue = $("#display_mobile_t").data("website");
    if (mobileValue) {
        $("#display_mobile_t").html('<strong>Mobile:</strong> ' + mobileValue);
    } else {
        $("#display_mobile_t").text("");
    }

    // Office
    var officeValue = $("#display_office_t").data("website");
    if (officeValue) {
        $("#display_office_t").html('<strong>Office:</strong> ' + officeValue);
    } else {
        $("#display_office_t").text("");
    }
});


// Personal Website
// Format the Personal Website URL and create a hyperlink
function formatPersonalWebsite(inputVal, iconColor) {
    var profileUrl = inputVal;
    var domain = new URL(inputVal).hostname;  // Extract domain using the URL object
    var iconHtml = '<i class="fa-solid fa-globe personal-icon" style="color:' + iconColor + ';"></i>';
    var colonHtml = '<span style="color: #000000;">:</span>';
    return iconHtml + ' ' + colonHtml + ' <a href="' + profileUrl + '" target="_blank">' + domain + '</a>';
}

$(document).ready(function() {
    // Fetch the color from the data-color attribute
    var iconColor = $("body").data("color");
    
    // Fetch the value from the data-website attribute
    var personalWebsiteValue = $("#display_personal_website").data("website").trim();

    // Display it
    if (personalWebsiteValue) {
        $("#display_personal_website").html(formatPersonalWebsite(personalWebsiteValue, iconColor));
    } else {
        $("#display_personal_website").text("");
    }
});


// Personal Twitter
// Format the Twitter URL and create a hyperlink
function formatTwitterLink(inputVal, iconColor) {
    // Extract the username from the URL. Assuming it's always valid.
    var username = inputVal.split('/').pop();
    var profileUrl = "https://twitter.com/" + username;
    var iconHtml = '<i class="fa-brands fa-twitter personal-icon" style="color:' + iconColor + ';"></i>';
    var colonHtml = '<span style="color: #000000;">:</span>';
    return iconHtml + ' ' + colonHtml + ' <a href="' + profileUrl + '" target="_blank">@' + username + '</a>';
}

$(document).ready(function() {
    // Fetch the color from the data-color attribute
    var iconColor = $("body").data("color");
    
    // Fetch the Twitter URL from the span content
    var twitterUrl = $("#display_personal_twitter").text().trim();

    // Display the formatted Twitter link
    $("#display_personal_twitter").html(formatTwitterLink(twitterUrl, iconColor));
});


// Personal Facebook
// Format the Facebook Profile URL and create a hyperlink
function formatPersonalFacebook(inputVal, iconColor) {
    var profileUrl = inputVal;
    var username = new URL(inputVal).pathname.substring(1);  // Extract username from the URL's pathname
    var iconHtml = '<i class="fa-brands fa-facebook personal-icon" style="color:' + iconColor + ';"></i>';
    var colonHtml = '<span style="color: #000000;">:</span>';
    return iconHtml + ' ' + colonHtml + ' <a href="' + profileUrl + '" target="_blank">' + username + '</a>';
}

$(document).ready(function() {
    // Fetch the color from the data-color attribute
    var iconColor = $("body").data("color");

    // Fetch the value from the data-website attribute for Facebook
    var personalFacebookValue = $("#display_personal_facebook").data("website").trim();

    // Display it
    if (personalFacebookValue) {
        $("#display_personal_facebook").html(formatPersonalFacebook(personalFacebookValue, iconColor));
    } else {
        $("#display_personal_facebook").text("");
    }
});


// Personal LinkedIn
// Format the LinkedIn Profile URL and create a hyperlink
function formatPersonalLinkedIn(inputVal, iconColor) {
    var profileUrl = inputVal;
    var username = new URL(inputVal).pathname.substring(1);  // Extract username from the URL's pathname
    var iconHtml = '<i class="fa-brands fa-linkedin personal-icon" style="color:' + iconColor + ';"></i>';
    var colonHtml = '<span style="color: #000000;">:</span>';
    return iconHtml + ' ' + colonHtml + ' <a href="' + profileUrl + '" target="_blank">' + username + '</a>';
}

$(document).ready(function() {
    // Fetch the color from the data-color attribute
    var iconColor = $("body").data("color");

    // Fetch the value from the data-website attribute for LinkedIn
    var personalLinkedInValue = $("#display_personal_linkedin").data("website").trim();

    // Display it
    if (personalLinkedInValue) {
        $("#display_personal_linkedin").html(formatPersonalLinkedIn(personalLinkedInValue, iconColor));
    } else {
        $("#display_personal_linkedin").text("");
    }
});


// Personal Instagram
// Format the Instagram Profile URL and create a hyperlink
function formatPersonalInstagram(inputVal, iconColor) {
    var profileUrl = inputVal;
    var username = new URL(inputVal).pathname.substring(1);  // Extract username from the URL's pathname (removing the leading '/')
    var iconHtml = '<i class="fa-brands fa-instagram personal-icon" style="color:' + iconColor + ';"></i>';
    var colonHtml = '<span style="color: #000000;">:</span>';
    return iconHtml + ' ' + colonHtml + ' <a href="' + profileUrl + '" target="_blank">' + username + '</a>';
}

$(document).ready(function() {
    // Fetch the color from the data-color attribute
    var iconColor = $("body").data("color");

    // Fetch the value from the data-website attribute for Instagram
    var personalInstagramValue = $("#display_personal_instagram").data("website").trim();

    // Display it
    if (personalInstagramValue) {
        $("#display_personal_instagram").html(formatPersonalInstagram(personalInstagramValue, iconColor));
    } else {
        $("#display_personal_instagram").text("");
    }
});


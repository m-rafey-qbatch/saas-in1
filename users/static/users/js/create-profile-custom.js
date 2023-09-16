$(document).ready(function() {

    if (initialFullName) {
        $("#display_full_name").text(initialFullName);
    } else {
        $("#display_full_name").text("Name");
    }

    $("#full_name").on('input', function() {
        var inputVal1 = $(this).val();
        if (inputVal1) {
            $("#display_full_name").text(inputVal1);
        } else {
            $("#display_full_name").text("Name");
        }
    });

    // Title
    // Set the initial value based on the input field
    var titleValue = $("#title").val();
    if (titleValue) {
        $("#display_title").text(titleValue);
    } else {
        $("#display_title").text("Title / Position");
    }

    // Update the display value when the input field changes
    $("#title").on('input', function() {
        var inputVal = $(this).val();
        if (inputVal) {
            $("#display_title").text(inputVal);
        } else {
            $("#display_title").text("Title / Position");
        }
    });


    $(document).ready(function() {
        // Mobile
        // Set the initial value based on the input field
        var mobileValue = $("#mobile").val();
        if (mobileValue) {
            $("#display_mobile").html('<strong>Mobile:</strong> ' + mobileValue);
        } else {
            $("#display_mobile").text("");
        }
    
        // Update the display value when the input field changes
        $("#mobile").on('input', function() {
            var inputVal = $(this).val();
            if (inputVal) {
                $("#display_mobile").html('<strong>Mobile:</strong> ' + inputVal);
            } else {
                $("#display_mobile").text("");
            }
        });
    });
    
    $(document).ready(function() {
        // Office - Disappear
        // Office - Set the initial value based on the input field
        var officeValue = $("#office").val();
        if (officeValue) {
            $("#display_office").html('<strong>Office:</strong> ' + officeValue);
        } else {
            $("#display_office").text("");
        }

        // Update the display value when the input field changes
        $("#office").on('input', function() {
            var inputVal = $(this).val();
            if (inputVal) {
                $("#display_office").html('<strong>Office:</strong> ' + inputVal);
            } else {
                $("#display_office").text("");
            }
        });
    });


    // Personal Website
    // Format the Personal Website URL and create a hyperlink
    function formatPersonalWebsite(inputVal) {
        // Regular expression to match a valid URL
        var urlRegex = /^(?:https?:\/\/)?(?:www\.)?([\w.-]+\.[a-zA-Z]{2,6})\/?([\w.-]*)?$/;
        
        if (urlRegex.test(inputVal)) {
            // Extract the domain and path from the URL
            var matches = inputVal.match(urlRegex);
            var domain = matches[1];
            var path = matches[2] ? '/' + matches[2] : '';
            var profileUrl = "https://" + domain + path;
            var iconHtml = '<i class="fa-solid fa-globe personal-icon"></i>';
            var colonHtml = '<span style="color: #000000;">:</span>';
            return iconHtml + ' ' + colonHtml + ' <a href="' + profileUrl + '" target="_blank">' + domain + '</a>';
        } else {
            return "";
        }
    }

    // Set the initial value based on the input field
    var personalWebsiteValue = $("#personal_website").val();
    personalWebsiteValue = personalWebsiteValue ? personalWebsiteValue.trim() : "";
    if (personalWebsiteValue) {
        $("#display_personal_website").html(formatPersonalWebsite(personalWebsiteValue));
    } else {
        $("#display_personal_website").text("");
    }

    // Update the display value when the input field changes
    $("#personal_website").on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal) {
            $("#display_personal_website").html(formatPersonalWebsite(inputVal));
        } else {
            $("#display_personal_website").text("");
        }
    });



    // Twitter
    // Format the Twitter URL and create a hyperlink
    function formatPersonalTwitter(inputVal) {
        // Regular expression to match a valid Twitter personal profile URL
        var twitterUrlRegex = /^(?:https?:\/\/)?(?:www\.)?twitter\.com\/([\w.-]+)\/?$/;

        if (twitterUrlRegex.test(inputVal)) {
            // Extract the username from the URL
            var username = inputVal.match(twitterUrlRegex)[1];
            var profileUrl = "https://twitter.com/" + username;
            var iconHtml = '<i class="fa-brands fa-x-twitter personal-icon"></i>';
            var colonHtml = '<span style="color: #000000;">:</span>';
            return iconHtml + ' ' + colonHtml + ' <a href="' + profileUrl + '" target="_blank">@' + username + '</a>';
        } else {
            return "";
        }
    }

    // Set the initial value based on the input field
    var personalTwitterValue = $("#personal_twitter").val();
    personalTwitterValue = personalTwitterValue ? personalTwitterValue.trim() : "";
    if (personalTwitterValue) {
        $("#display_personal_twitter").html(formatPersonalTwitter(personalTwitterValue));
    } else {
        $("#display_personal_twitter").text("");
    }

    // Update the display value when the input field changes
    $("#personal_twitter").on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal) {
            $("#display_personal_twitter").html(formatPersonalTwitter(inputVal));
        } else {
            $("#display_personal_twitter").text("");
        }
    });


    // Personal Facebook - Disappear
    // Format the Facebook URL and create a hyperlink
    function formatPersonalFacebook(inputVal) {
        // Regular expression to match a valid Facebook personal profile URL
        var facebookUrlRegex = /^(?:https?:\/\/)?(?:www\.)?facebook\.com\/([\w.-]+)\/?$/;

        if (facebookUrlRegex.test(inputVal)) {
            // Extract the username from the URL
            var username = inputVal.match(facebookUrlRegex)[1];
            var profileUrl = "https://www.facebook.com/" + username;
            var iconHtml = '<i class="fa-brands fa-facebook personal-icon"></i>';
            var colonHtml = '<span style="color: #000000;">:</span>';
            return iconHtml + ' <span>' + colonHtml + '</span> <a href="' + profileUrl + '" target="_blank">@' + username + '</a>';
        } else {
            return "";
        }
    }

    // Set the initial value based on the input field
    var personalFacebookValue = $("#personal_facebook").val();
    personalFacebookValue = personalFacebookValue ? personalFacebookValue.trim() : "";
    if (personalFacebookValue) {
        $("#display_personal_facebook").html(formatPersonalFacebook(personalFacebookValue));
    } else {
        $("#display_personal_facebook").text("");
    }

    // Update the display value when the input field changes
    $("#personal_facebook").on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal) {
            $("#display_personal_facebook").html(formatPersonalFacebook(inputVal));
        } else {
            $("#display_personal_facebook").text("");
        }
    });


    // Personal LinkedIn - Disappear
    // Format the LinkedIn URL and create a hyperlink
    function formatPersonalLinkedIn(inputVal) {
        // Regular expression to match a valid LinkedIn personal profile URL
        var linkedInUrlRegex = /^(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/([\w-]+)$/;

        if (linkedInUrlRegex.test(inputVal)) {
            // Extract the username from the URL
            var username = inputVal.match(linkedInUrlRegex)[1];
            var profileUrl = "https://www.linkedin.com/in/" + username;
            var iconHtml = '<i class="fa-brands fa-linkedin personal-icon"></i>';
            var colonHtml = '<span style="color: #000000;">:</span>';
            return iconHtml + ' <span>' + colonHtml + '</span> <a href="' + profileUrl + '" target="_blank">@' + username + '</a>';
        } else {
            return "";
        }
    }

    // Set the initial value based on the input field
    var personalLinkedInValue = $("#personal_linkedin").val();
    personalLinkedInValue = personalLinkedInValue ? personalLinkedInValue.trim() : "";
    if (personalLinkedInValue) {
        $("#display_personal_linkedin").html(formatPersonalLinkedIn(personalLinkedInValue));
    } else {
        $("#display_personal_linkedin").text("");
    }

    // Update the display value when the input field changes
    $("#personal_linkedin").on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal) {
            $("#display_personal_linkedin").html(formatPersonalLinkedIn(inputVal));
        } else {
            $("#display_personal_linkedin").text("");
        }
    });

    
    // Personal Instagram
    // Format the Instagram URL and create a hyperlink
    function formatPersonalInstagram(inputVal) {
        // Regular expression to match a valid Instagram personal profile URL
        var instagramUrlRegex = /^(?:https?:\/\/)?(?:www\.)?instagram\.com\/([\w.-]+)\/?$/;

        if (instagramUrlRegex.test(inputVal)) {
            // Extract the username from the URL
            var username = inputVal.match(instagramUrlRegex)[1];
            var profileUrl = "https://www.instagram.com/" + username;
            var iconHtml = '<i class="fa-brands fa-instagram personal-icon"></i>';
            var colonHtml = '<span style="color: #000000;">:</span>';
            return iconHtml + ' <span>' + colonHtml + '</span> <a href="' + profileUrl + '" target="_blank">@' + username + '</a>';
        } else {
            return ""; // No icon or text when the URL is invalid
        }
    }

    // Set the initial value based on the input field
    var personalInstagramValue = $("#personal_instagram").val();
    personalInstagramValue = personalInstagramValue ? personalInstagramValue.trim() : "";
    if (personalInstagramValue) {
        $("#display_personal_instagram").html(formatPersonalInstagram(personalInstagramValue));
    } else {
        $("#display_personal_instagram").text("");
    }

    // Update the display value when the input field changes
    $("#personal_instagram").on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal) {
            $("#display_personal_instagram").html(formatPersonalInstagram(inputVal));
        } else {
            $("#display_personal_instagram").text("");
        }
    });



    // BACKGROUND BORDER P COLOR
    // Function to update the icon colors, background color, and border color
    function updateColors(colorValue) {
        // Update the color of the icons in the personal profile section to match the selected color
        // $(".personal-icon.fa-brands, .personal-icon.fa-globe").css("color", colorValue);

        // Update the background color and border color
        $(".profile-info-container").css("background-color", colorValue);
        $(".profile-details-container").css("border-color", colorValue);
    }

    // Set the default background color on page load
    // Set the default background color and border color on page load
    var defaultColor = "#f8f9fa";
    $(".profile-info-container").css({
        "background-color": defaultColor,
    });
    $(".profile-details-container").css({
        "border-color": defaultColor,
    });

    // Apply the default color to the icons
    updateColors(defaultColor);

    $(".profile-info-container").addClass("dynamic-pbg-color");
    $(".profile-details-container").addClass("dynamic-pbd-color");

    // Function to get the CSRF token from the cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Get the CSRF token from the page's cookies
    var csrftoken = getCookie('csrftoken');

    // Listen for changes in the background color input field
    $("#p-color").on("change", function() {
        var colorValue = $(this).val();
        console.log("Color selected:", colorValue);

        fetch("/save_color/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-Requested-With': 'XMLHttpRequest', // Identify the request as AJAX
                "X-CSRFToken": csrftoken // Use the retrieved CSRF token
            },
            body: JSON.stringify({ color: colorValue })

        })
        .then(response => response.json())
        .then(data => {
            console.log("Color saved successfully:", data);
        })
        .catch(error => {
            console.log("Error saving color:", error);
        });

        $(".profile-info-container").css("background-color", colorValue);
        $(".profile-details-container").css("border-color", colorValue);

        // Update the icon colors, background color, and border color
        updateColors(colorValue);
    });


    var selectedColor = $("#selected-color").data('color') || defaultColor; // Use defaultColor if no color is selected
    updateColors(selectedColor); // Update colors based on the selected color






    // FONT COLOR
    // Function to update the Header Font Color
    function updateColorHeader (colorValueHeader) {
        // Update the Font Color
        $(".profile-info-container .full-name").css("color", colorValueHeader);
        $(".profile-info-container .title").css("color", colorValueHeader);
    }

    // Set the default background font color on page load
    var defaultColor = "#000000";
    $(".profile-info-container .full-name").css({
        "color": defaultColor,
    });
    $(".profile-info-container .title").css({
        "color": defaultColor,
    });

    // Apply the default font color
    updateColorHeader(defaultColor);

    $(".profile-info-container .full-name").addClass("dynamic-font-color");
    $(".profile-info-container .title").addClass("dynamic-font-color");

    // Function to get the CSRF token from the cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Get the CSRF token from the page's cookies
    var csrftoken = getCookie('csrftoken');

    // Listen for changes for the font color input
    $("#p-color-header").on("change", function() {
        var colorValueHeader = $(this).val();
        console.log("Font color selected:", colorValueHeader);

        fetch("/save_color_header/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-Requested-With': 'XMLHttpRequest', // Identify the request as AJAX
                "X-CSRFToken": csrftoken // Use the retrieved CSRF token
            },
            body: JSON.stringify({ colorHeader: colorValueHeader })

        })
        .then(response => response.json())
        .then(data => {
            console.log("Font color saved successfully:", data);
        })
        .catch(error => {
            console.log("Error saving font color:", error);
        });

        // Update Font Color with user Selection
        updateColorHeader(colorValueHeader);
    });


    var selectedColorHeader = $("#selected-color-header").data('colorHeader') || defaultColor; // Use defaultColor if no color is selected
    updateColorHeader(selectedColorHeader); // Update colors based on the selected color


    
});
    
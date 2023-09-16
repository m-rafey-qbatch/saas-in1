console.log("custom script running");

$(document).ready(function() {

    // COMPANY PROFILE PAGE

    // Company Name
    // Set the initial value based on the input field
    var compValue = $("#comp").val();
    if (compValue) {
        $("#display_comp").text(compValue);
    } else {
        $("#display_comp").text("Company Name");
    }
    $("#comp").on('input', function() {
        var inputVala = $(this).val();
        if (inputVala) {
            $("#display_comp").text(inputVala);
        } else {
            $("#display_comp").text("Company Name");
        }
    });



    // Company Website
    // Format the Company  Website URL and create a hyperlink
    function formatCompanyWebsite(inputVal) {
        // Regular expression to match a valid URL
        var urlRegex = /^(?:https?:\/\/)?(?:www\.)?([\w.-]+\.[a-zA-Z]{2,6})\/?([\w.-]*)?$/;
        
        if (urlRegex.test(inputVal)) {
            // Extract the domain and path from the URL
            var matches = inputVal.match(urlRegex);
            var domain = matches[1];
            var path = matches[2] ? '/' + matches[2] : '';
            var profileUrl = "https://" + domain + path;
            var iconHtml = '<i class="fa-solid fa-globe company-icon"></i>';
            var colonHtml = '<span style="color: #000000;">:</span>';
            return iconHtml + ' ' + colonHtml + ' <a href="' + profileUrl + '" target="_blank">' + domain + '</a>';
        } else {
            return "";
        }
    }

    // Set the initial value based on the input field
    var companyWebsiteValue = $("#company_website").val();
    companyWebsiteValue = companyWebsiteValue ? companyWebsiteValue.trim() : "";

    if (companyWebsiteValue) {
        $("#display_company_website").html(formatCompanyWebsite(companyWebsiteValue));
    } else {
        $("#display_company_website").text("");
    }

    // Update the display value when the input field changes

    $("#company_website").on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal) {
            $("#display_company_website").html(formatCompanyWebsite(inputVal));
        } else {
            $("#display_company_website").text("");
        }
    });


    // Company Address Street 1

    var co_street1Value = $("#co_street1").val();
    if (co_street1Value) {
        $("#display_co_street1").html('<strong>Address:</strong> ' + co_street1Value);
    } else {
        $("#display_co_street1").text("");
    }

    // Update the display value when the input field changes
    $("#co_street1").on('input', function() {
        var inputVal = $(this).val();
        if (inputVal) {
            $("#display_co_street1").html('<strong>Address:</strong> ' + inputVal);
        } else {
            $("#display_co_street1").text("");
        }
    });


    // Company Address Street 2
    // Set the initial value based on the input field
    var co_street2Value = $("#co_street2").val();
    if (co_street2Value) {
        $("#display_co_street2").text(co_street2Value);
    } else {
        $("#display_co_street2").text("");
    }

    // Update the display value when the input field changes
    $("#co_street2").on('input', function() {
        var inputVal = $(this).val();
        if (inputVal) {
            $("#display_co_street2").text(inputVal);
        } else {
            $("#display_co_street2").text("");
        }
    });


    // Company City
    var co_cityValue = $("#co_city").val();
    if (co_cityValue) {
        $("#display_co_city").html(co_cityValue  + ', ');
    } else {
        $("#display_co_city").text("");
    }

    // Update the display value when the input field changes
    $("#co_city").on('input', function() {
        var inputVal = $(this).val();
        if (inputVal) {
            $("#display_co_city").html(inputVal  + ', ');
        } else {
            $("#display_co_city").text("");
        }
    });

   
    // Company State
     var co_stateValue = $("#co_state").val();
     if (co_stateValue) {
         $("#display_co_state").text(co_stateValue);
     } else {
         $("#display_co_state").text("");
     }
 
     // Update the display value when the input field changes
     $("#co_state").on('input', function() {
         var inputVal = $(this).val();
         if (inputVal) {
             $("#display_co_state").text(inputVal);
         } else {
             $("#display_co_state").text("");
         }
     });



    // Company Zip

    var co_zip_codeValue = $("#co_zip_code").val();
     if (co_zip_codeValue) {
         $("#display_co_zip_code").text(co_zip_codeValue);
     } else {
         $("#display_co_zip_code").text("");
     }
 
     // Update the display value when the input field changes
     $("#co_zip_code").on('input', function() {
         var inputVal = $(this).val();
         if (inputVal) {
             $("#display_co_zip_code").text(inputVal);
         } else {
             $("#display_co_zip_code").text("");
         }
     });



    // Company Main Phone
    // Set the initial value based on the input field
    var co_phoneValue = $("#co_phone").val();
    if (co_phoneValue) {
        $("#display_co_phone").html('<strong>Company Main Phone:</strong> ' + co_phoneValue);
    } else {
        $("#display_co_phone").text("");
    }

    // Update the display value when the input field changes
    $("#co_phone").on('input', function() {
        var inputVal = $(this).val();
        if (inputVal) {
            $("#display_co_phone").html('<strong>Company Main Phone:</strong> ' + inputVal);
        } else {
            $("#display_co_phone").text("");
        }
    }); 


    // Company Email
    // Set the initial value based on the input field
    var co_emailValue = $("#co_email").val();
    if (co_emailValue) {
        $("#display_co_email").html('<strong>Company Email:</strong> ' + co_emailValue);
    } else {
        $("#display_co_email").text("");
    }

    // Update the display value when the input field changes
    $("#co_email").on('input', function() {
        var inputVal = $(this).val();
        if (inputVal) {
            $("#display_co_email").html('<strong>Company Email:</strong> <a target="_blank" href="mailto:' + inputVal + '">' + inputVal + '</a>');
        } else {
            $("#display_co_email").text("");
        }
    });




    // Company Fax
    var co_faxValue = $("#co_fax").val();
    if (co_faxValue) {
        $("#display_co_fax").html('<strong>Fax:</strong> ' + co_faxValue);
    } else {
        $("#display_co_fax").text("");
    }

    // Update the display value when the input field changes
    $("#co_fax").on('input', function() {
        var inputVal = $(this).val();
        if (inputVal) {
            $("#display_co_fax").html('<strong>Fax:</strong> ' + inputVal);
        } else {
            $("#display_co_fax").text("");
        }
    }); 
    
    

    // Company Twitter
    // Format the Twitter URL and create a hyperlink
    function formatCompanyTwitter(inputVal) {
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
    var companyTwitterValue = $("#co_twitter").val();
    companyTwitterValue = companyTwitterValue ? companyTwitterValue.trim() : "";
    if (companyTwitterValue) {
        $("#display_co_twitter").html(formatCompanyTwitter(companyTwitterValue));
    } else {
        $("#display_co_twitter").text("");
    }

    // Update the display value when the input field changes
    $("#co_twitter").on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal) {
            $("#display_co_twitter").html(formatCompanyTwitter(inputVal));
        } else {
            $("#display_co_twitter").text("");
        }
    });




     // Company Facebook
    // Format the Facebook URL and create a hyperlink
    function formatCompanyFacebook(inputVal) {
        // Regular expression to match a valid Facebook personal profile URL
        var facebookUrlRegex = /^(?:https?:\/\/)?(?:www\.)?facebook\.com\/([\w.-]+)\/?$/;

        if (facebookUrlRegex.test(inputVal)) {
            // Extract the username from the URL
            var username = inputVal.match(facebookUrlRegex)[1];
            var profileUrl = "https://www.facebook.com/" + username;
            var iconHtml = '<i class="fa-brands fa-facebook company-icon"></i>';
            var colonHtml = '<span style="color: #000000;">:</span>';
            return iconHtml + ' <span>' + colonHtml + '</span> <a href="' + profileUrl + '" target="_blank">@' + username + '</a>';
        } else {
            return "";
        }
    }

    // Set the initial value based on the input field
    var companyFacebookValue = $("#co_facebook").val();
    companyFacebookValue = companyFacebookValue ? companyFacebookValue.trim() : "";
    if (companyFacebookValue) {
        $("#display_co_facebook").html(formatCompanyFacebook(companyFacebookValue));
    } else {
        $("#display_co_facebook").text("");
    }

    // Update the display value when the input field changes
    $("#co_facebook").on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal) {
            $("#display_co_facebook").html(formatCompanyFacebook(inputVal));
        } else {
            $("#display_co_facebook").text("");
        }
    });




    // Company LinkedIn
    // Format the LinkedIn URL and create a hyperlink
    function formatCompanyLinkedIn(inputVal) {
        // Regular expression to match a valid LinkedIn personal profile URL
        var linkedInUrlRegex = /^(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/([\w-]+)$/;

        if (linkedInUrlRegex.test(inputVal)) {
            // Extract the username from the URL
            var username = inputVal.match(linkedInUrlRegex)[1];
            var profileUrl = "https://www.linkedin.com/in/" + username;
            var iconHtml = '<i class="fa-brands fa-linkedin company-icon"></i>';
            var colonHtml = '<span style="color: #000000;">:</span>';
            return iconHtml + ' <span>' + colonHtml + '</span> <a href="' + profileUrl + '" target="_blank">@' + username + '</a>';
        } else {
            return "";
        }
    }

    // Set the initial value based on the input field
    var companyLinkedInValue = $("#co_linkedin").val();
    companyLinkedInValue = companyLinkedInValue ? companyLinkedInValue.trim() : "";
    if (companyLinkedInValue) {
        $("#display_co_linkedin").html(formatCompanyLinkedIn(companyLinkedInValue));
    } else {
        $("#display_co_linkedin").text("");
    }

    // Update the display value when the input field changes
    $("#co_linkedin").on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal) {
            $("#display_co_linkedin").html(formatCompanyLinkedIn(inputVal));
        } else {
            $("#display_co_linkedin").text("");
        }
    });




    // Company Instagram
    // Format the Instagram URL and create a hyperlink
    function formatCompanyInstagram(inputVal) {
        // Regular expression to match a valid Instagram personal profile URL
        var instagramUrlRegex = /^(?:https?:\/\/)?(?:www\.)?instagram\.com\/([\w.-]+)\/?$/;

        if (instagramUrlRegex.test(inputVal)) {
            // Extract the username from the URL
            var username = inputVal.match(instagramUrlRegex)[1];
            var profileUrl = "https://www.instagram.com/" + username;
            var iconHtml = '<i class="fa-brands fa-instagram company-icon"></i>';
            var colonHtml = '<span style="color: #000000;">:</span>';
            return iconHtml + ' <span>' + colonHtml + '</span> <a href="' + profileUrl + '" target="_blank">@' + username + '</a>';
        } else {
            return ""; // No icon or text when the URL is invalid
        }
    }

    // Set the initial value based on the input field
    var companyInstagramValue = $("#co_instagram").val();
    companyInstagramValue = companyInstagramValue ? companyInstagramValue.trim() : "";
    if (companyInstagramValue) {
        $("#display_co_instagram").html(formatCompanyInstagram(companyInstagramValue));
    } else {
        $("#display_co_instagram").text("");
    }

    // Update the display value when the input field changes
    $("#co_instagram").on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal) {
            $("#display_co_instagram").html(formatCompanyInstagram(inputVal));
        } else {
            $("#display_co_instagram").text("");
        }
    });



    // COMPANY - BACKGROUND BORDER P COLOR
    // Function to update the icon colors, background color, and border color
    function updateCompanyColors(colorValue) {

        console.log('updateCompanyColors function called with colorValue:', colorValue);
    
        // Update the color of the icons in the company profile section to match the selected color
        // $(".company-icon.fa-brands").css("color", colorValue);
        
        // Update the background color and border color
        $(".company-info-container").css("background-color", colorValue);
        $(".company-details-container").css("border-color", colorValue);
    
    }

    // Set the default background color on page load
    // Set the default background color and border color on page load
    var defaultColor = "#f8f9fa";
    $(".company-info-container").css({
        "background-color": defaultColor,
    });

    $(".company-details-container").css({
        "border-color": defaultColor,
    });

    // Apply the default color to the icons
    updateCompanyColors(defaultColor);

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
    $("#c-color").on("change", function() {
        var colorValue = $(this).val();
        console.log("Color selected:", colorValue);

        fetch("/save_color_company/", {
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

        $(".company-info-container").css("background-color", colorValue);
        $(".company-details-container").css("border-color", colorValue);

        // Update the icon colors, background color, and border color
        updateCompanyColors(colorValue);
    });

    var selectedCompanyColor = $("#selected-color-company").data('color') || defaultColor; // Use defaultColor if no color is selected
    updateCompanyColors(selectedCompanyColor); // Update colors based on the selected color



    // COMPANY FONT COLOR
    // Function to update the Header Font Color
    function updateColorCoHeader (colorValueCoHeader) {
        // Update the Font Color
        $(".company-info-container .company-name").css("color", colorValueCoHeader);
        $(".company-info-container .company-website").css("color", colorValueCoHeader);
    }

    // Set the default background font color on page load
    var defaultCoColor = "#000000";
    

    // Apply the default font color
    updateColorCoHeader(defaultCoColor);

    $(".company-info-container .company-name").addClass("dynamic-font-co-color");
    $(".company-info-container .company-website").addClass("dynamic-font-co-color");

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
    $("#c-color-header").on("change", function() {
        var colorValueCoHeader = $(this).val();
        console.log("Font color selected:", colorValueCoHeader);

        fetch("/save_color_header_company/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-Requested-With': 'XMLHttpRequest', // Identify the request as AJAX
                "X-CSRFToken": csrftoken // Use the retrieved CSRF token
            },
            body: JSON.stringify({ colorCoHeader: colorValueCoHeader })

        })
        .then(response => response.json())
        .then(data => {
            console.log("Font color saved successfully:", data);
        })
        .catch(error => {
            console.log("Error saving font color:", error);
        });

        // Update Font Color with user Selection
        updateColorCoHeader(colorValueCoHeader);
    });


    var selectedColorCoHeader = $("#selected-color-header-company").data('colorCoHeader') || defaultCoColor; // Use defaultColor if no color is selected
    updateColorCoHeader(selectedColorCoHeader); // Update colors based on the selected color
   

    // COMPANY LOGO
    function readURL(input, displayElement) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
                console.log("File read successfully.");
                $(displayElement).attr('src', e.target.result);
            }

            console.log("Reading file...");
            reader.readAsDataURL(input.files[0]); // convert to base64 string
        }
    }

    $("#company_logo").change(function() {
        console.log("Company logo file input changed.");
        console.log(this);
        readURL(this, '#display_company_logo');
    });

    
});
    